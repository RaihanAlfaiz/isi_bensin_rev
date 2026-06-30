from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRectF, pyqtSignal, QPropertyAnimation, QPointF, QUrl
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap, QPainterPath, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QVideoSink, QAudioOutput
from config import BASE_DIR
import random
import math

class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(80)
        self.setFixedHeight(32)
        self.heights = [10.0, 15.0, 8.0, 20.0, 12.0]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_waveform)
        self.timer.start(100) # 10 fps for waveform bounce
        
    def update_waveform(self):
        for i in range(len(self.heights)):
            self.heights[i] = random.uniform(4.0, 28.0)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        bar_count = len(self.heights)
        bar_width = 4.0
        spacing = 6.0
        
        start_x = (w - (bar_count * bar_width + (bar_count - 1) * spacing)) / 2.0
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(78, 222, 163))) # neon green #4edea3
        
        for i, val in enumerate(self.heights):
            bx = start_x + i * (bar_width + spacing)
            by = (h - val) / 2.0
            painter.drawRoundedRect(QRectF(bx, by, bar_width, val), 2.0, 2.0)


class RFIDCardSensor(QWidget):
    frame_received = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.is_active = False
        self.target_w = 0
        self.target_h = 0
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0)
        self.media_player.setAudioOutput(self.audio_output)
        
        self.video_sink = QVideoSink()
        self.media_player.setVideoOutput(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.on_video_frame_changed)
        self.frame_received.connect(self.on_safe_frame_received)
        
        video_path = BASE_DIR / "resources" / "video" / "Kartu Tangan 1.mp4"
        self.media_player.setSource(QUrl.fromLocalFile(str(video_path)))
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)

    def showEvent(self, event):
        super().showEvent(event)
        self.is_active = True
        self.target_w = self.width()
        self.target_h = self.height()
        self.media_player.play()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.is_active = False
        self.media_player.stop()
        self.current_frame_image = None
        self.current_frame_pixmap = None

    def on_video_frame_changed(self, frame):
        if not self.is_active or not frame.isValid():
            return
        img = frame.toImage()
        if img.isNull():
            return
        w, h = self.target_w, self.target_h
        if w > 0 and h > 0:
            scaled_img = img.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.frame_received.emit(scaled_img)

    def on_safe_frame_received(self, image):
        self.current_frame_image = image
        self.current_frame_pixmap = QPixmap.fromImage(image)
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.target_w = size.width()
        self.target_h = size.height()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        if self.current_frame_pixmap and not self.current_frame_pixmap.isNull():
            tx = (rect.width() - self.current_frame_pixmap.width()) // 2
            ty = (rect.height() - self.current_frame_pixmap.height()) // 2
            painter.drawPixmap(tx, ty, self.current_frame_pixmap)
        else:
            cx = self.width() / 2.0
            cy = self.height() / 2.0
            
            card_w = 120.0
            card_h = 120.0
            card_rect = QRectF(cx - card_w/2.0, cy - card_h/2.0, card_w, card_h)
            
            painter.setPen(QPen(QColor(78, 222, 163, 60), 1.5))
            painter.setBrush(QBrush(QColor(78, 222, 163, 20)))
            painter.drawRoundedRect(card_rect, 16.0, 16.0)
            
            painter.setFont(QFont("Material Symbols Outlined", 64))
            painter.setPen(QColor(78, 222, 163))
            icon_text = "contactless"
            metrics = painter.fontMetrics()
            tx = cx - metrics.horizontalAdvance(icon_text) / 2.0
            ty = cy + (metrics.ascent() - metrics.descent()) / 2.0 - 5
            painter.drawText(int(tx), int(ty), icon_text)


class SuccessVideoWidget(QWidget):
    frame_received = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 180)
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.is_active = False
        self.target_w = 180
        self.target_h = 180
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0)
        self.media_player.setAudioOutput(self.audio_output)
        
        self.video_sink = QVideoSink()
        self.media_player.setVideoOutput(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.on_video_frame_changed)
        self.frame_received.connect(self.on_safe_frame_received)
        
        video_path = BASE_DIR / "resources" / "video" / "Tangan Hp 1.mp4"
        self.media_player.setSource(QUrl.fromLocalFile(str(video_path)))
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)

    def showEvent(self, event):
        super().showEvent(event)
        self.is_active = True
        self.target_w = self.width()
        self.target_h = self.height()
        self.media_player.play()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.is_active = False
        self.media_player.stop()
        self.current_frame_image = None
        self.current_frame_pixmap = None

    def on_video_frame_changed(self, frame):
        if not self.is_active or not frame.isValid():
            return
        img = frame.toImage()
        if img.isNull():
            return
        w, h = self.target_w, self.target_h
        if w > 0 and h > 0:
            scaled_img = img.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.frame_received.emit(scaled_img)

    def on_safe_frame_received(self, image):
        self.current_frame_image = image
        self.current_frame_pixmap = QPixmap.fromImage(image)
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.target_w = size.width()
        self.target_h = size.height()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        if self.current_frame_pixmap and not self.current_frame_pixmap.isNull():
            tx = (rect.width() - self.current_frame_pixmap.width()) // 2
            ty = (rect.height() - self.current_frame_pixmap.height()) // 2
            painter.drawPixmap(tx, ty, self.current_frame_pixmap)



class QRScannerVisual(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(180, 180)
        self.scan_line_y = 0.0
        self.scan_direction = 1.0
        
        # Load local QR code image
        self.pixmap = QPixmap(str(BASE_DIR / "resources" / "images" / "qr_code.png"))
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(25) # ~40 fps
        
    def animate(self):
        h = self.height() - 20
        if h <= 0:
            return
            
        self.scan_line_y += self.scan_direction * 2.0
        if self.scan_line_y >= h:
            self.scan_line_y = h
            self.scan_direction = -1.0
        elif self.scan_line_y <= 0:
            self.scan_line_y = 0
            self.scan_direction = 1.0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        size = min(w, h) - 20
        x = (w - size) / 2.0
        y = (h - size) / 2.0
        rect = QRectF(x, y, size, size)
        
        # Draw rounded bounding box
        painter.setPen(QPen(QColor(0, 240, 255, 40), 1.5))
        painter.setBrush(QBrush(QColor(255, 255, 255, 5)))
        painter.drawRoundedRect(rect, 16.0, 16.0)
        
        # Clip inside for QR code
        path = QPainterPath()
        path.addRoundedRect(rect.adjusted(1, 1, -1, -1), 15.0, 15.0)
        painter.save()
        painter.setClipPath(path)
        
        # Draw QR code image
        if not self.pixmap.isNull():
            painter.drawPixmap(rect.toRect(), self.pixmap)
        else:
            # Fallback mock QR code drawing if image is missing
            painter.fillRect(rect, QColor(6, 14, 32))
            painter.setPen(QPen(QColor(0, 240, 255, 100), 2.0))
            # draw simple grid
            step = int(size / 6)
            for i in range(1, 6):
                painter.drawLine(int(x + i*step), int(y), int(x + i*step), int(y + size))
                painter.drawLine(int(x), int(y + i*step), int(x + size), int(y + i*step))
                
        # Draw scan line
        ly = y + (self.scan_line_y / (self.height() - 20)) * size
        painter.setPen(QPen(QColor(0, 240, 255), 2.5))
        painter.drawLine(int(x), int(ly), int(x + size), int(ly))
        
        # Draw neon scan glow under the line
        painter.fillRect(QRectF(x, ly - 6, size, 6), QColor(0, 240, 255, 40))
        
        painter.restore()


class ClickableBentoBox(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            ClickableBentoBox {
                background-color: rgba(45, 52, 73, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 32px;
                text-align: center;
            }
            ClickableBentoBox:hover {
                background-color: rgba(45, 52, 73, 0.65);
                border: 1px solid rgba(0, 240, 255, 0.25);
            }
            ClickableBentoBox:pressed {
                background-color: rgba(45, 52, 73, 0.8);
            }
        """)
        
    def sizeHint(self):
        lay = self.layout()
        if lay:
            return lay.sizeHint()
        return super().sizeHint()

    def minimumSizeHint(self):
        lay = self.layout()
        if lay:
            return lay.minimumSize()
        return super().minimumSizeHint()


class PaymentState(QWidget):
    payment_completed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        self.is_processing = False
        
        self.setup_ui()
        self.update_language("en")
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 20)
        layout.setSpacing(24)
        
        # 1. Header Context
        header_row = QHBoxLayout()
        header_row.setSpacing(12)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        self.header_title = QLabel("Payment Required")
        self.header_title.setFont(QFont("Space Grotesk", 28, QFont.Weight.Bold))
        self.header_title.setStyleSheet("color: #dbfcff; background: transparent;")
        
        self.header_sub = QLabel("Select your preferred payment method to begin charging.")
        self.header_sub.setFont(QFont("Inter", 12))
        self.header_sub.setStyleSheet("color: #b9cacb; background: transparent;")
        
        title_layout.addWidget(self.header_title)
        title_layout.addWidget(self.header_sub)
        
        # Estimated Total
        self.est_container = QWidget()
        self.est_container.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 52, 73, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
            }
        """)
        self.est_container.setFixedHeight(64)
        
        est_layout = QVBoxLayout(self.est_container)
        est_layout.setContentsMargins(20, 10, 20, 10)
        est_layout.setSpacing(2)
        est_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.est_lbl = QLabel("ESTIMATED TOTAL")
        self.est_lbl.setFont(QFont("Space Grotesk", 9, QFont.Weight.Bold))
        self.est_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none; letter-spacing: 1px;")
        
        self.est_val = QLabel("$34.50")
        self.est_val.setFont(QFont("Space Grotesk", 20, QFont.Weight.Bold))
        self.est_val.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        
        est_layout.addWidget(self.est_lbl)
        est_layout.addWidget(self.est_val)
        
        header_row.addLayout(title_layout)
        header_row.addStretch()
        header_row.addWidget(self.est_container)
        layout.addLayout(header_row)
        
        # 2. Bento Grid (RFID / QR)
        bento_row = QHBoxLayout()
        bento_row.setSpacing(24)
        
        # RFID Bento Card
        self.rfid_card = ClickableBentoBox()
        self.rfid_card.clicked.connect(self.simulate_payment)
        
        rfid_layout = QVBoxLayout(self.rfid_card)
        rfid_layout.setContentsMargins(24, 24, 24, 24)
        rfid_layout.setSpacing(16)
        rfid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.rfid_sensor = RFIDCardSensor()
        self.rfid_title = QLabel("TAP RFID")
        self.rfid_title.setFont(QFont("Space Grotesk", 20, QFont.Weight.Bold))
        self.rfid_title.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        self.rfid_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.rfid_desc = QLabel("Hold your member card or mobile wallet near the reader below the screen.")
        self.rfid_desc.setFont(QFont("Inter", 11))
        self.rfid_desc.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        self.rfid_desc.setWordWrap(True)
        self.rfid_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Interaction Hint
        self.sensing_pill = QWidget()
        self.sensing_pill.setStyleSheet("""
            QWidget {
                background-color: rgba(78, 222, 163, 0.1);
                border: 1px solid rgba(78, 222, 163, 0.3);
                border-radius: 16px;
            }
        """)
        self.sensing_pill.setFixedHeight(32)
        sensing_layout = QHBoxLayout(self.sensing_pill)
        sensing_layout.setContentsMargins(16, 0, 16, 0)
        self.sensing_lbl = QLabel("SENSING...")
        self.sensing_lbl.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        self.sensing_lbl.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 1.5px;")
        self.sensing_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sensing_layout.addWidget(self.sensing_lbl)
        
        rfid_layout.addWidget(self.rfid_sensor, 1)
        rfid_layout.addWidget(self.rfid_title)
        rfid_layout.addWidget(self.rfid_desc)
        rfid_layout.addWidget(self.sensing_pill, 0, Qt.AlignmentFlag.AlignCenter)
        
        # QR Bento Card
        self.qr_card = ClickableBentoBox()
        self.qr_card.clicked.connect(self.simulate_payment)
        
        qr_layout = QVBoxLayout(self.qr_card)
        qr_layout.setContentsMargins(24, 24, 24, 24)
        qr_layout.setSpacing(16)
        qr_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.qr_visual = QRScannerVisual()
        self.qr_title = QLabel("QR SCAN")
        self.qr_title.setFont(QFont("Space Grotesk", 20, QFont.Weight.Bold))
        self.qr_title.setStyleSheet("color: #00dbe9; background: transparent; border: none;")
        self.qr_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.qr_desc = QLabel("Scan the code with the VOLTCORE app or your camera to pay via web.")
        self.qr_desc.setFont(QFont("Inter", 11))
        self.qr_desc.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        self.qr_desc.setWordWrap(True)
        self.qr_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Session Hint
        self.session_pill = QWidget()
        self.session_pill.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }
        """)
        self.session_pill.setFixedHeight(32)
        session_layout = QHBoxLayout(self.session_pill)
        session_layout.setContentsMargins(16, 0, 16, 0)
        self.session_lbl = QLabel("SESSION #4882")
        self.session_lbl.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        self.session_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none; letter-spacing: 1px;")
        self.session_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        session_layout.addWidget(self.session_lbl)
        
        qr_layout.addWidget(self.qr_visual, 1)
        qr_layout.addWidget(self.qr_title)
        qr_layout.addWidget(self.qr_desc)
        qr_layout.addWidget(self.session_pill, 0, Qt.AlignmentFlag.AlignCenter)
        
        bento_row.addWidget(self.rfid_card)
        bento_row.addWidget(self.qr_card)
        layout.addLayout(bento_row, 1)
        
        # 3. Footer Notification (Audio Waveform Guidance)
        self.footer = QWidget()
        self.footer.setStyleSheet("background: transparent;")
        footer_layout = QVBoxLayout(self.footer)
        footer_layout.setContentsMargins(0, 12, 0, 0)
        footer_layout.setSpacing(16)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.footer_instruction = QLabel("TEMPELKAN KARTU")
        self.footer_instruction.setFont(QFont("Space Grotesk", 24, QFont.Weight.Bold))
        self.footer_instruction.setStyleSheet("color: #ffffff; background: transparent; letter-spacing: 2px;")
        self.footer_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Audio voice container
        self.audio_pill = QWidget()
        self.audio_pill.setFixedHeight(72)
        self.audio_pill.setMinimumWidth(480)
        self.audio_pill.setStyleSheet("""
            QWidget {
                background-color: rgba(23, 31, 51, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 36px;
            }
        """)
        
        audio_layout = QHBoxLayout(self.audio_pill)
        audio_layout.setContentsMargins(24, 0, 24, 0)
        audio_layout.setSpacing(16)
        
        self.waveform = WaveformWidget()
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.voice_active_lbl = QLabel("VOICE GUIDANCE ACTIVE")
        self.voice_active_lbl.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        self.voice_active_lbl.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 1.5px;")
        
        self.voice_desc_lbl = QLabel('"Please tap your payment card on the reader to continue."')
        self.voice_desc_lbl.setFont(QFont("Inter", 10))
        self.voice_desc_lbl.setStyleSheet("color: rgba(185, 202, 203, 0.75); background: transparent; border: none;")
        
        text_layout.addWidget(self.voice_active_lbl)
        text_layout.addWidget(self.voice_desc_lbl)
        
        speaker_icon = QLabel("volume_up")
        speaker_icon.setFont(QFont("Material Symbols Outlined", 24))
        speaker_icon.setStyleSheet("color: rgba(185, 202, 203, 0.4); background: transparent; border: none;")
        
        audio_layout.addWidget(self.waveform)
        audio_layout.addLayout(text_layout, 1)
        audio_layout.addWidget(speaker_icon)
        
        footer_layout.addWidget(self.footer_instruction)
        footer_layout.addWidget(self.audio_pill, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.footer)
        
        # 4. Success Overlay Dialog (hidden by default)
        self.success_overlay = QWidget(self)
        self.success_overlay.setVisible(False)
        self.success_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(11, 19, 38, 0.95);
            }
        """)
        
        overlay_layout = QVBoxLayout(self.success_overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.setSpacing(20)
        
        self.success_video = SuccessVideoWidget()
        
        self.success_title = QLabel("PAYMENT SUCCESSFUL")
        self.success_title.setFont(QFont("Space Grotesk", 28, QFont.Weight.Bold))
        self.success_title.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        self.success_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.success_desc = QLabel("Starting charging session... Please wait.")
        self.success_desc.setFont(QFont("Inter", 14))
        self.success_desc.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        self.success_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        overlay_layout.addWidget(self.success_video, 0, Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(self.success_title)
        overlay_layout.addWidget(self.success_desc)
        
        # Connect success overlay size matching
        self.success_overlay.setGeometry(self.rect())
        
    def simulate_payment(self):
        if self.is_processing:
            return
        self.is_processing = True
        self.sensing_lbl.setText("PROCESSING...")
        self.sensing_lbl.setStyleSheet("color: #00dbe9; background: transparent; border: none; letter-spacing: 1.5px;")
        self.sensing_pill.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 240, 255, 0.1);
                border: 1px solid rgba(0, 240, 255, 0.3);
                border-radius: 16px;
            }
        """)
        
        # Wait 1.5 seconds and trigger success dialog
        QTimer.singleShot(1500, self.show_success_dialog)
        
    def show_success_dialog(self):
        self.success_overlay.setGeometry(self.rect())
        self.success_overlay.setVisible(True)
        self.success_overlay.raise_()
        
        # Wait 2.5 seconds and transition back/complete payment
        QTimer.singleShot(2500, self.finish_payment)
        
    def finish_payment(self):
        self.success_overlay.setVisible(False)
        self.is_processing = False
        
        # Reset labels
        self.sensing_lbl.setText("SENSING...")
        self.sensing_lbl.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 1.5px;")
        self.sensing_pill.setStyleSheet("""
            QWidget {
                background-color: rgba(78, 222, 163, 0.1);
                border: 1px solid rgba(78, 222, 163, 0.3);
                border-radius: 16px;
            }
        """)
        
        self.payment_completed.emit()
        
    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.header_title.setText("Payment Required")
            self.header_sub.setText("Select your preferred payment method to begin charging.")
            self.est_lbl.setText("ESTIMATED TOTAL")
            self.est_val.setText("$34.50")
            
            self.rfid_title.setText("TAP RFID")
            self.rfid_desc.setText("Hold your member card or mobile wallet near the reader below the screen.")
            self.sensing_lbl.setText("SENSING..." if not self.is_processing else "PROCESSING...")
            
            self.qr_title.setText("QR SCAN")
            self.qr_desc.setText("Scan the code with the VOLTCORE app or your camera to pay via web.")
            self.session_lbl.setText("SESSION #4882")
            
            self.footer_instruction.setText("TAP YOUR CARD")
            self.voice_active_lbl.setText("VOICE GUIDANCE ACTIVE")
            self.voice_desc_lbl.setText('"Please tap your payment card on the reader to continue."')
            
            self.success_title.setText("PAYMENT SUCCESSFUL")
            self.success_desc.setText("Starting charging session... Please wait.")
        else: # id
            self.header_title.setText("Pembayaran Diperlukan")
            self.header_sub.setText("Pilih metode pembayaran yang Anda inginkan untuk memulai pengisian.")
            self.est_lbl.setText("ESTIMASI TOTAL")
            self.est_val.setText("Rp 517.500")
            
            self.rfid_title.setText("TEMPEL RFID")
            self.rfid_desc.setText("Tempelkan kartu anggota atau dompet digital Anda dekat alat pembaca di bawah layar.")
            self.sensing_lbl.setText("MENDETEKSI..." if not self.is_processing else "MEMPROSES...")
            
            self.qr_title.setText("PINDAI QR")
            self.qr_desc.setText("Pindai kode dengan aplikasi VOLTCORE atau kamera Anda untuk membayar via web.")
            self.session_lbl.setText("SESI #4882")
            
            self.footer_instruction.setText("TEMPELKAN KARTU")
            self.voice_active_lbl.setText("PANDUAN SUARA AKTIF")
            self.voice_desc_lbl.setText('"Silakan tempelkan kartu pembayaran Anda pada alat pembaca untuk melanjutkan."')
            
            self.success_title.setText("PEMBAYARAN BERHASIL")
            self.success_desc.setText("Memulai sesi pengisian daya... Harap tunggu.")
            
    def resizeEvent(self, event):
        self.success_overlay.setGeometry(self.rect())
        super().resizeEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        painter.fillRect(rect, QColor("#0b1326"))
        
        # Draw background radial gradient glow
        from PyQt6.QtGui import QRadialGradient
        glow = QRadialGradient(float(rect.width()/2.0), float(rect.height()/2.0), float(min(rect.width(), rect.height())) * 0.6)
        glow.setColorAt(0.0, QColor(0, 240, 255, 12))  # cyan glow 5%
        glow.setColorAt(0.6, QColor(78, 222, 163, 4))
        glow.setColorAt(1.0, Qt.GlobalColor.transparent)
        painter.fillRect(rect, glow)
        
        super().paintEvent(event)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QTimer, QUrl, QRectF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QLinearGradient, QImage, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QVideoSink
from config import BASE_DIR
import math

class FinishedVideoCard(QWidget):
    frame_received = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("right_card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget#right_card {
                background: rgba(23, 31, 51, 0.7);
                border: 1px solid rgba(78, 222, 163, 0.08);
                border-radius: 24px;
            }
        """)
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.is_active = False
        self.target_w = 0
        self.target_h = 0
        
        self.media_player = QMediaPlayer()
        self.video_sink = QVideoSink()
        self.media_player.setVideoOutput(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.on_video_frame_changed)
        self.frame_received.connect(self.on_safe_frame_received)
        
        video_path = BASE_DIR / "resources" / "video" / "Animasi Selesai Cas Mobil.mp4"
        self.media_player.setSource(QUrl.fromLocalFile(str(video_path)))
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)
        
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
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.frame_received.emit(scaled_img)

    def on_safe_frame_received(self, img):
        self.current_frame_image = img
        self.current_frame_pixmap = QPixmap.fromImage(img)
        self.update()

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.target_w = size.width()
        self.target_h = size.height()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # 1. Rounded Clip Path for the video card
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 24.0, 24.0)
        
        # Draw background color
        painter.fillPath(path, QBrush(QColor(23, 31, 51, int(255 * 0.7))))
        
        # 2. Draw current frame
        if self.current_frame_pixmap is not None and not self.current_frame_pixmap.isNull():
            painter.save()
            painter.setClipPath(path)
            x = (rect.width() - self.current_frame_pixmap.width()) // 2
            y = (rect.height() - self.current_frame_pixmap.height()) // 2
            painter.drawPixmap(x, y, self.current_frame_pixmap)
            painter.restore()
                
        # 3. Draw border
        painter.setPen(QPen(QColor(78, 222, 163, int(255 * 0.08)), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5), 24.0, 24.0)




class DetailRow(QWidget):
    def __init__(self, icon_str, title_str, val_str, unit_str="", parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("DetailRow")
        self.setMinimumHeight(64)
        
        self.normal_style = """
            QWidget#DetailRow {
                background: transparent;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
        """
        self.hover_style = """
            QWidget#DetailRow {
                background: rgba(78, 222, 163, 0.04);
                border-bottom: 1px solid rgba(78, 222, 163, 0.25);
                border-radius: 8px;
            }
        """
        self.setStyleSheet(self.normal_style)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)
        
        self.icon_lbl = QLabel(icon_str)
        self.icon_lbl.setFont(QFont("Material Symbols Outlined", 20))
        self.icon_lbl.setStyleSheet("color: #4edea3; opacity: 0.7; background: transparent;")
        
        self.title_lbl = QLabel(title_str)
        self.title_lbl.setFont(QFont("Inter", 14))
        self.title_lbl.setStyleSheet("color: #b9cacb; background: transparent;")
        
        self.val_lbl = QLabel(val_str)
        self.val_lbl.setFont(QFont("Space Grotesk", 20, QFont.Weight.Bold))
        self.val_lbl.setStyleSheet("color: #ffffff; background: transparent;")
        
        self.unit_lbl = QLabel(unit_str)
        self.unit_lbl.setFont(QFont("Inter", 12))
        self.unit_lbl.setStyleSheet("color: #b9cacb; background: transparent; margin-bottom: 2px;")
        
        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.title_lbl)
        layout.addStretch()
        layout.addWidget(self.val_lbl)
        if unit_str:
            layout.addWidget(self.unit_lbl)
            
    def set_value(self, val_str):
        self.val_lbl.setText(val_str)
        
    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        self.icon_lbl.setStyleSheet("color: #4edea3; opacity: 1.0; background: transparent;")
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.setStyleSheet(self.normal_style)
        self.icon_lbl.setStyleSheet("color: #4edea3; opacity: 0.7; background: transparent;")
        super().leaveEvent(event)


class FinishingState(QWidget):
    finish_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        
        # Default/Initial variables to display
        self.final_time_sec = 3732  # 01:02:12
        self.final_energy_kwh = 12.4
        self.price_per_kwh = 2500
        
        self.setup_ui()
        self.update_language("en")
        
    def set_session_details(self, elapsed_seconds, energy_kwh, price_per_kwh=2500):
        self.final_time_sec = elapsed_seconds
        self.final_energy_kwh = energy_kwh
        self.price_per_kwh = price_per_kwh
        self.update_values()
        
    def update_values(self):
        # Format time
        h = self.final_time_sec // 3600
        m = (self.final_time_sec % 3600) // 60
        s = self.final_time_sec % 60
        self.time_row.set_value(f"{h:02d}:{m:02d}:{s:02d}")
        
        # Energy
        self.energy_row.set_value(f"{self.final_energy_kwh:.1f}")
        
        # Cost (energy * price_per_kwh IDR/kWh)
        cost_val = int(self.final_energy_kwh * self.price_per_kwh)
        # format as Indonesian Rupiah
        cost_formatted = f"Rp {cost_val:,}".replace(",", ".")
        self.cost_row.set_value(cost_formatted)
        
        # CO2 saved (energy * 0.338 kg/kWh)
        co2_saved = self.final_energy_kwh * 0.338
        self.co2_row.set_value(f"{co2_saved:.1f}")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 36, 40, 36)
        main_layout.setSpacing(24)
        
        # 1. Header (Transaction Summary & Ready to Unplug Status)
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        title_box.setSpacing(6)
        
        self.subtitle_lbl = QLabel("TRANSACTION SUMMARY")
        self.subtitle_lbl.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        self.subtitle_lbl.setStyleSheet("color: #4edea3; letter-spacing: 2px; background: transparent;")
        
        self.title_lbl = QLabel("Charging Summary")
        self.title_lbl.setFont(QFont("Plus Jakarta Sans", 32, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #dbfcff; background: transparent;")
        
        title_box.addWidget(self.subtitle_lbl)
        title_box.addWidget(self.title_lbl)
        
        # Badge "Ready to Unplug"
        self.badge_widget = QWidget()
        self.badge_widget.setStyleSheet("""
            QWidget {
                background: rgba(23, 31, 51, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
            }
        """)
        badge_layout = QHBoxLayout(self.badge_widget)
        badge_layout.setContentsMargins(20, 10, 20, 10)
        badge_layout.setSpacing(10)
        
        # Green Dot Indicator
        self.dot_lbl = QLabel()
        self.dot_lbl.setFixedSize(10, 10)
        self.dot_lbl.setStyleSheet("background-color: #4edea3; border-radius: 5px;")
        
        self.badge_txt = QLabel("Ready to Unplug")
        self.badge_txt.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        self.badge_txt.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 0.5px;")
        
        badge_layout.addWidget(self.dot_lbl)
        badge_layout.addWidget(self.badge_txt)
        
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        header_layout.addWidget(self.badge_widget, 0, Qt.AlignmentFlag.AlignVCenter)
        
        main_layout.addLayout(header_layout)
        
        # 2. Columns (Left: Summary, Right: Eco Graph)
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(28)
        
        # Left Bento Card (Summary Details)
        self.left_card = QWidget()
        self.left_card.setObjectName("left_card")
        self.left_card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.left_card.setStyleSheet("""
            QWidget#left_card {
                background: rgba(23, 31, 51, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 24px;
            }
        """)
        left_layout = QVBoxLayout(self.left_card)
        left_layout.setContentsMargins(28, 28, 28, 28)
        left_layout.setSpacing(16)
        
        # Rows
        self.time_row = DetailRow("schedule", "Total Time", "01:02:12")
        self.energy_row = DetailRow("bolt", "Energy", "12.4", "kWh")
        self.cost_row = DetailRow("payments", "Cost", "Rp 31.000")
        self.co2_row = DetailRow("eco", "CO₂ Saved", "4.2", "kg")
        
        left_layout.addWidget(self.time_row)
        left_layout.addWidget(self.energy_row)
        left_layout.addWidget(self.cost_row)
        left_layout.addWidget(self.co2_row)
        
        left_layout.addSpacing(12)
        
        # Audio Notice Box at bottom of left card
        self.audio_box = QWidget()
        self.audio_box.setStyleSheet("""
            QWidget {
                background-color: rgba(78, 222, 163, 0.08);
                border: 1px solid rgba(78, 222, 163, 0.2);
                border-radius: 16px;
            }
        """)
        audio_layout = QHBoxLayout(self.audio_box)
        audio_layout.setContentsMargins(16, 16, 16, 16)
        audio_layout.setSpacing(16)
        
        audio_btn = QWidget()
        audio_btn.setFixedSize(36, 36)
        audio_btn.setStyleSheet("background-color: #4edea3; border-radius: 10px;")
        audio_btn_layout = QHBoxLayout(audio_btn)
        audio_btn_layout.setContentsMargins(0, 0, 0, 0)
        audio_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        audio_icon = QLabel("volume_up")
        audio_icon.setFont(QFont("Material Symbols Outlined", 18))
        audio_icon.setStyleSheet("color: #00311f; background: transparent;")
        audio_btn_layout.addWidget(audio_icon)
        
        self.audio_txt = QLabel('"Please unplug your vehicle"')
        self.audio_txt.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        self.audio_txt.setStyleSheet("color: #4edea3; background: transparent; border: none; font-style: italic;")
        
        audio_layout.addWidget(audio_btn)
        audio_layout.addWidget(self.audio_txt, 1)
        
        left_layout.addWidget(self.audio_box)
               # Right Bento Card (Finished Video Card)
        self.right_card = FinishedVideoCard()
        
        columns_layout.addWidget(self.left_card, 7)
        columns_layout.addWidget(self.right_card, 5)
        
        main_layout.addLayout(columns_layout, 1)
        
        # 3. Persistent Bottom Action Buttons (Print Receipt & Finish Transaction)
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(24)
        
        self.print_btn = QPushButton("Print Receipt")
        self.print_btn.setFont(QFont("Space Grotesk", 13, QFont.Weight.Bold))
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.print_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 2px solid #849495;
                border-radius: 16px;
                color: #dae2fd;
                min-height: 52px;
                padding-left: 36px;
                padding-right: 36px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.05);
                border-color: #ffffff;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        self.finish_btn = QPushButton("Finish Transaction")
        self.finish_btn.setFont(QFont("Space Grotesk", 13, QFont.Weight.Bold))
        self.finish_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.finish_btn.clicked.connect(self.on_finish_clicked)
        self.finish_btn.setStyleSheet("""
            QPushButton {
                background-color: #00dbe9;
                border: none;
                border-radius: 16px;
                color: #002022;
                min-height: 52px;
                padding-left: 40px;
                padding-right: 40px;
            }
            QPushButton:hover {
                background-color: #00f0ff;
            }
            QPushButton:pressed {
                background-color: #00b8c4;
            }
        """)
        
        footer_layout.addStretch()
        footer_layout.addWidget(self.print_btn)
        footer_layout.addWidget(self.finish_btn)
        
        main_layout.addLayout(footer_layout)
        
    def on_finish_clicked(self):
        self.finish_clicked.emit()
        
    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.subtitle_lbl.setText("TRANSACTION SUMMARY")
            self.title_lbl.setText("Charging Summary")
            self.badge_txt.setText("Ready to Unplug")
            self.time_row.title_lbl.setText("Total Time")
            self.energy_row.title_lbl.setText("Energy")
            self.cost_row.title_lbl.setText("Cost")
            self.co2_row.title_lbl.setText("CO₂ Saved")
            self.audio_txt.setText('"Please unplug your vehicle"')
            self.print_btn.setText("Print Receipt")
            self.finish_btn.setText("Finish Transaction")
        else: # id
            self.subtitle_lbl.setText("RINGKASAN TRANSAKSI")
            self.title_lbl.setText("Informasi Pengisian")
            self.badge_txt.setText("Ready to Unplug")
            self.time_row.title_lbl.setText("Total Waktu")
            self.energy_row.title_lbl.setText("Energi")
            self.cost_row.title_lbl.setText("Biaya")
            self.co2_row.title_lbl.setText("CO₂ Saved")
            self.audio_txt.setText('"Silakan cabut kendaraan Anda"')
            self.print_btn.setText("Print Receipt")
            self.finish_btn.setText("Finish Transaction")
            
        self.update_values()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        painter.fillRect(rect, QColor("#0b1326"))
        
        # Radial background gradient
        glow = QLinearGradient(0, 0, rect.width(), rect.height())
        glow.setColorAt(0.0, QColor(0, 240, 255, 8))
        glow.setColorAt(0.5, QColor(78, 222, 163, 4))
        glow.setColorAt(1.0, Qt.GlobalColor.transparent)
        painter.fillRect(rect, glow)
        
        super().paintEvent(event)

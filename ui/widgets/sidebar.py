from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QRectF, pyqtSignal, QUrl
from PyQt6.QtGui import QPainter, QColor, QFont, QFontDatabase, QPixmap, QBrush, QPen, QPainterPath, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink
from config import BASE_DIR

class SidebarLastTxCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        self.session_data = {
            "date": "18 Jun 2026",
            "time": "14:35 WIB",
            "soc": "85%",
            "energy": "20.4 kWh",
            "duration": "01:35:12",
            "cost": "Rp 51.000"
        }
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 52, 73, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        
        header = QHBoxLayout()
        header.setSpacing(6)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        icon = QLabel("history")
        icon.setFont(QFont("Material Symbols Outlined", 14))
        icon.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        
        self.title_lbl = QLabel("LAST TRANSACTION")
        self.title_lbl.setFont(QFont("Space Grotesk", 9, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 1.0px;")
        
        header.addWidget(icon)
        header.addWidget(self.title_lbl)
        layout.addLayout(header)
        
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent; border: none;")
        self.grid = QGridLayout(grid_widget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(2)
        
        self.lbl_date = QLabel("Date:")
        self.val_date = QLabel()
        self.lbl_time = QLabel("Time:")
        self.val_time = QLabel()
        self.lbl_soc = QLabel("SOC:")
        self.val_soc = QLabel()
        
        self.lbl_energy = QLabel("Energy:")
        self.val_energy = QLabel()
        self.lbl_dur = QLabel("Duration:")
        self.val_dur = QLabel()
        self.lbl_cost = QLabel("Cost:")
        self.val_cost = QLabel()
        
        label_style = "color: #b9cacb; opacity: 0.6; background: transparent; border: none;"
        value_style = "color: #ffffff; background: transparent; border: none; font-weight: bold;"
        
        for lbl in [self.lbl_date, self.lbl_time, self.lbl_soc, self.lbl_energy, self.lbl_dur, self.lbl_cost]:
            lbl.setFont(QFont("Inter", 8))
            lbl.setStyleSheet(label_style)
            
        for val in [self.val_date, self.val_time, self.val_soc, self.val_energy, self.val_dur, self.val_cost]:
            val.setFont(QFont("Space Grotesk", 8))
            val.setStyleSheet(value_style)
            
        self.grid.addWidget(self.lbl_date, 0, 0)
        self.grid.addWidget(self.val_date, 0, 1)
        self.grid.addWidget(self.lbl_time, 1, 0)
        self.grid.addWidget(self.val_time, 1, 1)
        self.grid.addWidget(self.lbl_soc, 2, 0)
        self.grid.addWidget(self.val_soc, 2, 1)
        
        self.grid.addWidget(self.lbl_energy, 0, 2)
        self.grid.addWidget(self.val_energy, 0, 3)
        self.grid.addWidget(self.lbl_dur, 1, 2)
        self.grid.addWidget(self.val_dur, 1, 3)
        self.grid.addWidget(self.lbl_cost, 2, 2)
        self.grid.addWidget(self.val_cost, 2, 3)
        
        layout.addWidget(grid_widget)
        self.refresh_display()
        
    def update_session(self, date, time, soc, energy, duration, cost):
        self.session_data = {
            "date": date,
            "time": time,
            "soc": soc,
            "energy": energy,
            "duration": duration,
            "cost": cost
        }
        self.refresh_display()
        
    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.title_lbl.setText("LAST TRANSACTION")
            self.lbl_date.setText("Date:")
            self.lbl_time.setText("Time:")
            self.lbl_soc.setText("SOC:")
            self.lbl_energy.setText("Energy:")
            self.lbl_dur.setText("Dur:")
            self.lbl_cost.setText("Cost:")
        else:
            self.title_lbl.setText("TRANSAKSI TERAKHIR")
            self.lbl_date.setText("Tanggal:")
            self.lbl_time.setText("Waktu:")
            self.lbl_soc.setText("SOC:")
            self.lbl_energy.setText("Energi:")
            self.lbl_dur.setText("Durasi:")
            self.lbl_cost.setText("Biaya:")
        self.refresh_display()
        
    def refresh_display(self):
        d = self.session_data
        self.val_date.setText(d["date"])
        self.val_time.setText(d["time"])
        self.val_soc.setText(d["soc"])
        self.val_energy.setText(d["energy"])
        self.val_dur.setText(d["duration"])
        self.val_cost.setText(d["cost"])

class SidebarReservationCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        self.status = "Reserved"
        self.user = "Booked by User"
        self.start_time = "Start Time: 14:30 WIB"
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(178, 89, 0, 0.15);
                border: 1px solid rgba(255, 170, 68, 0.3);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        header = QHBoxLayout()
        header.setSpacing(6)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.icon = QLabel("bookmark")
        self.icon.setFont(QFont("Material Symbols Outlined", 14))
        self.icon.setStyleSheet("color: #ffaa44; background: transparent; border: none;")
        
        self.title_lbl = QLabel("RESERVATION INFO")
        self.title_lbl.setFont(QFont("Space Grotesk", 9, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #ffaa44; background: transparent; border: none; letter-spacing: 1px;")
        
        header.addWidget(self.icon)
        header.addWidget(self.title_lbl)
        layout.addLayout(header)
        
        self.status_lbl = QLabel()
        self.status_lbl.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        self.status_lbl.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        
        self.user_lbl = QLabel()
        self.user_lbl.setFont(QFont("Inter", 9))
        self.user_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        self.time_lbl = QLabel()
        self.time_lbl.setFont(QFont("Inter", 9))
        self.time_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        layout.addWidget(self.status_lbl)
        layout.addWidget(self.user_lbl)
        layout.addWidget(self.time_lbl)
        
        self.refresh_display()
        
    def set_reservation_details(self, status_str, user_str, time_str):
        self.status = status_str
        self.user = user_str
        self.start_time = time_str
        
        # Adjust stylesheet depending on Scheduled vs Reserved
        if "Scheduled" in status_str or "Terjadwal" in status_str:
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(58, 63, 88, 0.25);
                    border: 1px solid rgba(143, 158, 255, 0.3);
                    border-radius: 12px;
                }
            """)
            self.icon.setStyleSheet("color: #8f9eff; background: transparent; border: none;")
            self.title_lbl.setStyleSheet("color: #8f9eff; background: transparent; border: none; letter-spacing: 1px;")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(178, 89, 0, 0.15);
                    border: 1px solid rgba(255, 170, 68, 0.3);
                    border-radius: 12px;
                }
            """)
            self.icon.setStyleSheet("color: #ffaa44; background: transparent; border: none;")
            self.title_lbl.setStyleSheet("color: #ffaa44; background: transparent; border: none; letter-spacing: 1px;")
            
        self.refresh_display()
        
    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.title_lbl.setText("RESERVATION INFO")
        else:
            self.title_lbl.setText("INFO RESERVASI")
        self.refresh_display()
        
    def refresh_display(self):
        status_text = self.status
        user_text = self.user
        time_text = self.start_time
        
        if self.current_lang != "en":
            if status_text == "Reserved":
                status_text = "Dipesan"
            elif status_text == "Scheduled":
                status_text = "Terjadwal"
                
            if user_text == "Booked by User":
                user_text = "Dipesan oleh Pengguna"
            elif user_text == "Scheduled Session":
                user_text = "Sesi Terjadwal"
                
            if "Start Time:" in time_text:
                time_text = time_text.replace("Start Time:", "Waktu Mulai:")
                
        self.status_lbl.setText(status_text)
        self.user_lbl.setText(user_text)
        self.time_lbl.setText(time_text)

class SidebarQueueCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        self.waiting_users = 2
        self.est_wait = 20
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 219, 233, 0.08);
                border: 1px solid rgba(0, 219, 233, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        header = QHBoxLayout()
        header.setSpacing(6)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        icon = QLabel("people")
        icon.setFont(QFont("Material Symbols Outlined", 14))
        icon.setStyleSheet("color: #00dbe9; background: transparent; border: none;")
        
        self.title_lbl = QLabel("QUEUE STATUS")
        self.title_lbl.setFont(QFont("Space Grotesk", 9, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #00dbe9; background: transparent; border: none; letter-spacing: 1px;")
        
        header.addWidget(icon)
        header.addWidget(self.title_lbl)
        layout.addLayout(header)
        
        self.users_lbl = QLabel()
        self.users_lbl.setFont(QFont("Inter", 9))
        self.users_lbl.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        
        self.wait_lbl = QLabel()
        self.wait_lbl.setFont(QFont("Inter", 9))
        self.wait_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        layout.addWidget(self.users_lbl)
        layout.addWidget(self.wait_lbl)
        
        self.refresh_display()
        
    def set_queue_details(self, users, wait_minutes):
        self.waiting_users = users
        self.est_wait = wait_minutes
        self.refresh_display()
        
    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.title_lbl.setText("QUEUE STATUS")
        else:
            self.title_lbl.setText("STATUS ANTREAN")
        self.refresh_display()
        
    def refresh_display(self):
        if self.current_lang == "en":
            self.users_lbl.setText(f"Waiting Users: {self.waiting_users}")
            self.wait_lbl.setText(f"Estimated Wait: {self.est_wait} Minutes")
        else:
            self.users_lbl.setText(f"Pengguna Antre: {self.waiting_users}")
            self.wait_lbl.setText(f"Estimasi Tunggu: {self.est_wait} Menit")

class SidebarStatusBox(QWidget):
    frame_received = pyqtSignal(QImage)
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(140, 140)
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.is_active = False
        self.target_w = 140
        self.target_h = 140
        self.bg_color = QColor("#00a572")
        self.border_color = QColor("rgba(78, 222, 163, 0.5)")
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0)
        self.media_player.setAudioOutput(self.audio_output)
        
        self.video_sink = QVideoSink()
        self.media_player.setVideoOutput(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.on_video_frame_changed)
        self.frame_received.connect(self.on_safe_frame_received)
        
        self.current_video_file = None
        
        # Child widgets
        box_layout = QVBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.setSpacing(8)
 
        self.charger_icon = QLabel("ev_charger")
        self.charger_icon.setFont(QFont("Material Symbols Outlined", 48))
        self.charger_icon.setStyleSheet("color: #00311f; background: transparent; border: none;")
        self.charger_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        self.status_txt = QLabel("Status")
        self.status_txt.setFont(QFont("Space Grotesk", 16, QFont.Weight.Bold))
        self.status_txt.setStyleSheet("color: #00311f; background: transparent; border: none;")
        self.status_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        box_layout.addWidget(self.charger_icon)
        box_layout.addWidget(self.status_txt)
 
        self.status_sub_txt = QLabel("PREPARING")
        sub_font = QFont("Space Grotesk", 10, QFont.Weight.Bold)
        sub_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115)
        self.status_sub_txt.setFont(sub_font)
        self.status_sub_txt.setStyleSheet("color: rgba(0, 49, 31, 204); background: transparent; border: none;")
        self.status_sub_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_sub_txt.setVisible(False)
        box_layout.addWidget(self.status_sub_txt)
 
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
        
    def set_style(self, bg_color_str, border_color_str):
        self.bg_color = QColor(bg_color_str)
        self.border_color = QColor(border_color_str)
        self.update()
        
    def showEvent(self, event):
        super().showEvent(event)
        self.is_active = True
        self.target_w = self.width()
        self.target_h = self.height()
        if self.current_video_file:
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
        
    def set_video(self, video_filename):
        if video_filename:
            video_path = BASE_DIR / "resources" / "video" / video_filename
            if video_path.exists():
                url = QUrl.fromLocalFile(str(video_path))
                if self.current_video_file != video_filename:
                    self.current_video_file = video_filename
                    self.media_player.stop()
                    self.media_player.setSource(url)
                    self.media_player.setLoops(QMediaPlayer.Loops.Infinite)
                    if self.is_active:
                        self.media_player.play()
                self.charger_icon.setVisible(False)
                self.status_txt.setVisible(False)
                self.status_sub_txt.setVisible(False)
                return
        
        self.media_player.stop()
        self.current_video_file = None
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.charger_icon.setVisible(True)
        self.status_txt.setVisible(True)
        self.update()
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Background path
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 16.0, 16.0)
        
        # Fill background
        painter.fillPath(path, QBrush(self.bg_color))
        
        # If video frame exists, draw it inside the border (with clipping)
        if self.current_frame_pixmap is not None and not self.current_frame_pixmap.isNull():
            painter.save()
            painter.setClipPath(path)
            painter.drawPixmap(rect, self.current_frame_pixmap)
            painter.restore()
            
        # Draw border
        painter.setPen(QPen(self.border_color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(rect).adjusted(1, 1, -1, -1), 16.0, 16.0)


class Sidebar(QWidget):
    language_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        
        self.current_lang = "en"
        self.status_state = "idle"
        self.setMinimumWidth(220)
        self.setMaximumWidth(280)
        
        self.queue_active = True
        self.waiting_users = 2
        self.est_wait_time = 20

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 36, 20, 36)
        layout.setSpacing(24)

        # 1. Brand Identity (Top)
        brand_container = QWidget()
        brand_container.setStyleSheet("background: transparent;")
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(8)
        brand_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_lbl = QLabel()
        logo_pixmap = QPixmap(str(BASE_DIR / "resources" / "icon" / "logoputih-removebg-preview.png"))
        if not logo_pixmap.isNull():
            logo_lbl.setPixmap(logo_pixmap.scaled(70, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_lbl.setStyleSheet("background: transparent; border: none;")

        self.station_lbl = QLabel("Station ID: 4882-X")
        self.station_lbl.setFont(QFont("Inter", 12))
        self.station_lbl.setStyleSheet("color: #b9cacb; opacity: 0.7; background: transparent;")
        self.station_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand_layout.addWidget(logo_lbl)
        brand_layout.addWidget(self.station_lbl)
        layout.addWidget(brand_container)

        # 2. Global Status Indicator (Middle)
        status_container = QWidget()
        status_container.setStyleSheet("background: transparent;")
        status_layout = QVBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(12)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Status Box
        self.status_box = SidebarStatusBox()
        self.charger_icon = self.status_box.charger_icon
        self.status_txt = self.status_box.status_txt
        self.status_sub_txt = self.status_box.status_sub_txt

        # Status pulse glow animation
        shadow = QGraphicsDropShadowEffect(self.status_box)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(78, 222, 163, 120))
        shadow.setOffset(0, 0)
        self.status_box.setGraphicsEffect(shadow)
        self.shadow_effect = shadow

        # Static shadow glow to prevent layout recalculation jitter
        shadow.setBlurRadius(15)

        # Text below box
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.available_lbl = QLabel("AVAILABLE")
        self.available_lbl.setFont(QFont("Space Grotesk", 18, QFont.Weight.Bold))
        self.available_lbl.setStyleSheet("color: #4edea3; background: transparent;")
        self.available_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ready_lbl = QLabel("Ready to charge")
        self.ready_lbl.setFont(QFont("Inter", 11))
        self.ready_lbl.setStyleSheet("color: #b9cacb; background: transparent;")
        self.ready_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ready_lbl.setWordWrap(True)

        text_layout.addWidget(self.available_lbl)
        text_layout.addWidget(self.ready_lbl)

        status_layout.addWidget(self.status_box)
        status_layout.addLayout(text_layout)
        layout.addWidget(status_container)

        # 2.5 Dynamic Info Panels Container
        self.info_container = QWidget()
        self.info_container.setStyleSheet("background: transparent;")
        info_layout = QVBoxLayout(self.info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(10)
        
        self.last_tx_card = SidebarLastTxCard()
        self.reservation_card = SidebarReservationCard()
        self.queue_card = SidebarQueueCard()
        
        info_layout.addWidget(self.last_tx_card)
        info_layout.addWidget(self.reservation_card)
        info_layout.addWidget(self.queue_card)
        
        layout.addWidget(self.info_container)

        # Stretch spacing
        layout.addStretch()

        # 3. Language Selector Footer (Bottom)
        footer_container = QWidget()
        footer_container.setStyleSheet("background: transparent;")
        footer_layout = QVBoxLayout(footer_container)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)

        # Stylesheet for buttons
        btn_style = """
            QPushButton {
                background-color: rgba(45, 52, 73, 0.2);
                border: 1px solid rgba(59, 73, 75, 0.2);
                border-radius: 12px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: rgba(45, 52, 73, 0.5);
                border-color: rgba(78, 222, 163, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(45, 52, 73, 0.7);
            }
        """

        self.lang_btn = QPushButton()
        self.lang_btn.setStyleSheet(btn_style)
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lang_layout = QHBoxLayout(self.lang_btn)
        lang_layout.setContentsMargins(12, 0, 12, 0)
        lang_layout.setSpacing(8)
        lang_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lang_icon = QLabel("language")
        lang_icon.setFont(QFont("Material Symbols Outlined", 18))
        lang_icon.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        self.lang_txt = QLabel("English")
        self.lang_txt.setFont(QFont("Space Grotesk", 12, QFont.Weight.Bold))
        self.lang_txt.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        lang_layout.addWidget(lang_icon)
        lang_layout.addWidget(self.lang_txt)

        self.settings_btn = QPushButton()
        self.settings_btn.setStyleSheet(btn_style)
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_layout = QHBoxLayout(self.settings_btn)
        settings_layout.setContentsMargins(12, 0, 12, 0)
        settings_layout.setSpacing(8)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        settings_icon = QLabel("settings")
        settings_icon.setFont(QFont("Material Symbols Outlined", 18))
        settings_icon.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        self.settings_txt = QLabel("Settings")
        self.settings_txt.setFont(QFont("Space Grotesk", 12, QFont.Weight.Bold))
        self.settings_txt.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        settings_layout.addWidget(settings_icon)
        settings_layout.addWidget(self.settings_txt)

        footer_layout.addWidget(self.lang_btn)
        footer_layout.addWidget(self.settings_btn)
        layout.addWidget(footer_container)

        self.lang_btn.clicked.connect(self.toggle_language)
        self.refresh_status_text()
        self.update_sidebar_panels()

    def toggle_language(self):
        if self.current_lang == "en":
            self.current_lang = "id"
        else:
            self.current_lang = "en"
        self.language_changed.emit(self.current_lang)

    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.lang_txt.setText("English")
            self.settings_txt.setText("Settings")
        else:  # id
            self.lang_txt.setText("Indonesia")
            self.settings_txt.setText("Pengaturan")
            
        self.last_tx_card.update_language(lang)
        self.reservation_card.update_language(lang)
        self.queue_card.update_language(lang)
        self.refresh_status_text()
        self.update_sidebar_panels()

    def set_status_state(self, state):
        self.status_state = state
        self.refresh_status_text()
        self.update_sidebar_panels()

    def update_queue_info(self, active, users=2, wait_time=20):
        self.queue_active = active
        self.waiting_users = users
        self.est_wait_time = wait_time
        self.queue_card.set_queue_details(users, wait_time)
        self.update_sidebar_panels()

    def update_last_transaction(self, date, time, soc, energy, duration, cost):
        self.last_tx_card.update_session(date, time, soc, energy, duration, cost)

    def update_sidebar_panels(self):
        # 1. Last transaction card
        if self.status_state in ["idle", "available"]:
            self.last_tx_card.setVisible(True)
        else:
            self.last_tx_card.setVisible(False)
            
        # 2. Reservation card
        if self.status_state in ["reserved", "scheduled"]:
            self.reservation_card.setVisible(True)
        else:
            self.reservation_card.setVisible(False)
            
        # 3. Queue card
        if self.queue_active:
            self.queue_card.setVisible(True)
        else:
            self.queue_card.setVisible(False)

    def refresh_status_text(self):
        # Setup specific theme properties for each status
        state_config = {
            "idle": {
                "bg": "#00a572", "border": "rgba(78, 222, 163, 0.5)", "text_color": "#00311f", 
                "glow": QColor(78, 222, 163, 120), "icon": "ev_charger", "sub_visible": False,
                "lbl_main_en": "AVAILABLE", "lbl_main_id": "TERSEDIA", "lbl_main_color": "#4edea3",
                "lbl_desc_en": "Ready to charge", "lbl_desc_id": "Siap untuk mengisi daya",
                "video_file": "Status.mp4"
            },
            "available": {
                "bg": "#00a572", "border": "rgba(78, 222, 163, 0.5)", "text_color": "#00311f", 
                "glow": QColor(78, 222, 163, 120), "icon": "ev_charger", "sub_visible": False,
                "lbl_main_en": "AVAILABLE", "lbl_main_id": "TERSEDIA", "lbl_main_color": "#4edea3",
                "lbl_desc_en": "Ready to charge", "lbl_desc_id": "Siap untuk mengisi daya",
                "video_file": "Status.mp4"
            },
            "preparing": {
                "bg": "#008080", "border": "rgba(0, 240, 255, 0.5)", "text_color": "#002a2b", 
                "glow": QColor(0, 240, 255, 120), "icon": "power", "sub_visible": False,
                "lbl_main_en": "PREPARING", "lbl_main_id": "MENYIAPKAN", "lbl_main_color": "#00f0ff",
                "lbl_desc_en": "Preparing connector...", "lbl_desc_id": "Menyiapkan konektor...",
                "video_file": "Status Oren 1.mp4"
            },
            "charging": {
                "bg": "#0a5c8c", "border": "rgba(0, 219, 233, 0.5)", "text_color": "#ffffff", 
                "glow": QColor(0, 219, 233, 120), "icon": "bolt", "sub_visible": False,
                "lbl_main_en": "CHARGING", "lbl_main_id": "PENGISIAN", "lbl_main_color": "#00dbe9",
                "lbl_desc_en": "Charging vehicle...", "lbl_desc_id": "Mengisi daya kendaraan...",
                "video_file": "Charging 1.mp4"
            },
            "finishing": {
                "bg": "#5c2d91", "border": "rgba(181, 124, 255, 0.5)", "text_color": "#ffffff", 
                "glow": QColor(181, 124, 255, 120), "icon": "done_all", "sub_visible": False,
                "lbl_main_en": "FINISHING", "lbl_main_id": "SELESAI", "lbl_main_color": "#b57cff",
                "lbl_desc_en": "Session completed", "lbl_desc_id": "Sesi selesai",
                "video_file": "Charging State(1).mp4"
            },
            "reserved": {
                "bg": "#b25900", "border": "rgba(255, 170, 68, 0.5)", "text_color": "#3a1c00", 
                "glow": QColor(255, 170, 68, 120), "icon": "bookmark", "sub_visible": False,
                "lbl_main_en": "RESERVED", "lbl_main_id": "DIPESAN", "lbl_main_color": "#ffaa44",
                "lbl_desc_en": "Reserved for user", "lbl_desc_id": "Dipesan oleh pengguna"
            },
            "scheduled": {
                "bg": "#3a3f58", "border": "rgba(143, 158, 255, 0.5)", "text_color": "#ffffff", 
                "glow": QColor(143, 158, 255, 120), "icon": "schedule", "sub_visible": False,
                "lbl_main_en": "SCHEDULED", "lbl_main_id": "TERJADWAL", "lbl_main_color": "#8f9eff",
                "lbl_desc_en": "Scheduled session", "lbl_desc_id": "Sesi terjadwal"
            },
            "faulted": {
                "bg": "#a61c1c", "border": "rgba(255, 123, 123, 0.5)", "text_color": "#ffffff", 
                "glow": QColor(255, 123, 123, 120), "icon": "warning", "sub_visible": False,
                "lbl_main_en": "FAULTED", "lbl_main_id": "GANGGUAN", "lbl_main_color": "#ff7b7b",
                "lbl_desc_en": "System error detected", "lbl_desc_id": "Gangguan sistem terdeteksi"
            },
            "transaction": {
                "bg": "#008080", "border": "rgba(0, 240, 255, 0.5)", "text_color": "#002a2b", 
                "glow": QColor(0, 240, 255, 120), "icon": "payments", "sub_visible": False,
                "lbl_main_en": "TRANSACTION", "lbl_main_id": "TRANSAKSI", "lbl_main_color": "#00f0ff",
                "lbl_desc_en": "Processing payment...", "lbl_desc_id": "Memproses pembayaran...",
                "video_file": "Transaksi 1.mp4"
            }
        }
        
        cfg = state_config.get(self.status_state, state_config["idle"])
        
        # Apply Box Styling
        self.status_box.set_style(cfg["bg"], cfg["border"])
        self.status_box.set_video(cfg.get("video_file"))
        
        self.charger_icon.setText(cfg["icon"])
        self.charger_icon.setStyleSheet(f"color: {cfg['text_color']}; background: transparent; border: none;")
        self.status_txt.setStyleSheet(f"color: {cfg['text_color']}; background: transparent; border: none;")
        
        # Apply Text Below Box
        main_text = cfg["lbl_main_en"] if self.current_lang == "en" else cfg["lbl_main_id"]
        desc_text = cfg["lbl_desc_en"] if self.current_lang == "en" else cfg["lbl_desc_id"]
        
        self.available_lbl.setText(main_text)
        self.available_lbl.setStyleSheet(f"color: {cfg['lbl_main_color']}; background: transparent;")
        
        self.ready_lbl.setText(desc_text)
        
        # Update Shadow Glow
        self.shadow_effect.setColor(cfg["glow"])

    def set_station_id(self, station_id):
        self.station_lbl.setText(f"Station ID: {station_id}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Sidebar background (#060e20)
        painter.fillRect(self.rect(), QColor("#060e20"))
        
        # Right border line (#3b494b with 20% opacity)
        painter.setPen(QColor(59, 73, 75, 50))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        
        super().paintEvent(event)
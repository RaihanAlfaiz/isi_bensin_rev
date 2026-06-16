from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QFontDatabase, QPixmap
from config import BASE_DIR

class Sidebar(QWidget):
    # Signal to notify when language changes ('en' or 'id')
    language_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        
        self.current_lang = "en"
        self.status_state = "idle"
        self.setMinimumWidth(220)
        self.setMaximumWidth(280)

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 48, 24, 48)
        layout.setSpacing(32)

        # 1. Brand Identity (Top)
        brand_container = QWidget()
        brand_container.setStyleSheet("background: transparent;")
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(10)
        brand_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_lbl = QLabel()
        logo_pixmap = QPixmap(str(BASE_DIR / "resources" / "icon" / "logoputih-removebg-preview.png"))
        if not logo_pixmap.isNull():
            logo_lbl.setPixmap(logo_pixmap.scaled(70, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_lbl.setStyleSheet("background: transparent; border: none;")

        station_lbl = QLabel("Station ID: 4882-X")
        station_lbl.setFont(QFont("Inter", 12))
        station_lbl.setStyleSheet("color: #b9cacb; opacity: 0.7; background: transparent;")
        station_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand_layout.addWidget(logo_lbl)
        brand_layout.addWidget(station_lbl)
        layout.addWidget(brand_container)

        # 2. Global Status Indicator (Middle)
        status_container = QWidget()
        status_container.setStyleSheet("background: transparent;")
        status_layout = QVBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(16)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Status Box
        self.status_box = QWidget()
        self.status_box.setFixedSize(140, 140)
        self.status_box.setStyleSheet("""
            QWidget {
                background-color: #00a572;
                border: 2px solid rgba(78, 222, 163, 0.5);
                border-radius: 16px;
            }
        """)

        box_layout = QVBoxLayout(self.status_box)
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

        # Status pulse glow animation
        shadow = QGraphicsDropShadowEffect(self.status_box)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(78, 222, 163, 120))
        shadow.setOffset(0, 0)
        self.status_box.setGraphicsEffect(shadow)

        self.pulse_anim = QPropertyAnimation(shadow, b"blurRadius")
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setKeyValueAt(0.5, 25)
        self.pulse_anim.setEndValue(10)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.start()

        # Text below box
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.available_lbl = QLabel("AVAILABLE")
        self.available_lbl.setFont(QFont("Space Grotesk", 20, QFont.Weight.Bold))
        self.available_lbl.setStyleSheet("color: #4edea3; background: transparent;")
        self.available_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ready_lbl = QLabel("Ready to charge")
        self.ready_lbl.setFont(QFont("Inter", 12))
        self.ready_lbl.setStyleSheet("color: #b9cacb; background: transparent;")
        self.ready_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ready_lbl.setWordWrap(True)

        text_layout.addWidget(self.available_lbl)
        text_layout.addWidget(self.ready_lbl)

        status_layout.addWidget(self.status_box)
        status_layout.addLayout(text_layout)
        layout.addWidget(status_container)

        # Stretch spacing
        layout.addStretch()

        # 3. Language Selector Footer (Bottom)
        footer_container = QWidget()
        footer_container.setStyleSheet("background: transparent;")
        footer_layout = QVBoxLayout(footer_container)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(12)

        # Stylesheet for buttons
        btn_style = """
            QPushButton {
                background-color: rgba(45, 52, 73, 0.2);
                border: 1px solid rgba(59, 73, 75, 0.2);
                border-radius: 12px;
                min-height: 48px;
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
        lang_layout.setContentsMargins(16, 0, 16, 0)
        lang_layout.setSpacing(12)
        lang_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lang_icon = QLabel("language")
        lang_icon.setFont(QFont("Material Symbols Outlined", 20))
        lang_icon.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        self.lang_txt = QLabel("English")
        self.lang_txt.setFont(QFont("Space Grotesk", 14, QFont.Weight.Bold))
        self.lang_txt.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        lang_layout.addWidget(lang_icon)
        lang_layout.addWidget(self.lang_txt)

        self.settings_btn = QPushButton()
        self.settings_btn.setStyleSheet(btn_style)
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_layout = QHBoxLayout(self.settings_btn)
        settings_layout.setContentsMargins(16, 0, 16, 0)
        settings_layout.setSpacing(12)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        settings_icon = QLabel("settings")
        settings_icon.setFont(QFont("Material Symbols Outlined", 20))
        settings_icon.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        self.settings_txt = QLabel("Settings")
        self.settings_txt.setFont(QFont("Space Grotesk", 14, QFont.Weight.Bold))
        self.settings_txt.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        settings_layout.addWidget(settings_icon)
        settings_layout.addWidget(self.settings_txt)

        footer_layout.addWidget(self.lang_btn)
        footer_layout.addWidget(self.settings_btn)
        layout.addWidget(footer_container)

        # Connect language button click to toggle method
        self.lang_btn.clicked.connect(self.toggle_language)

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
            self.available_lbl.setText("AVAILABLE")
            self.ready_lbl.setText("Ready to charge")
        else:  # id
            self.lang_txt.setText("Indonesia")
            self.settings_txt.setText("Pengaturan")
            self.available_lbl.setText("TERSEDIA")
            self.ready_lbl.setText("Siap untuk mengisi daya")
        self.refresh_status_text()

    def set_status_state(self, state):
        self.status_state = state
        self.refresh_status_text()

    def refresh_status_text(self):
        if self.status_state == "idle":
            self.status_sub_txt.setVisible(False)
            self.available_lbl.setVisible(True)
            self.ready_lbl.setVisible(True)
            self.charger_icon.setText("ev_charger")
            self.status_txt.setText("Status")
            self.status_box.setStyleSheet("""
                QWidget {
                    background-color: #00a572;
                    border: 2px solid rgba(78, 222, 163, 0.5);
                    border-radius: 16px;
                }
            """)
        elif self.status_state == "preparing":
            self.status_sub_txt.setVisible(True)
            self.status_sub_txt.setText("PREPARING" if self.current_lang == "en" else "MEMPERSIAPKAN")
            self.available_lbl.setVisible(False)
            self.ready_lbl.setVisible(False)
            self.charger_icon.setText("ev_charger")
            self.status_txt.setText("Status")
            self.status_box.setStyleSheet("""
                QWidget {
                    background-color: #00a572;
                    border: 2px solid rgba(78, 222, 163, 0.5);
                    border-radius: 16px;
                }
            """)
        elif self.status_state == "transaction":
            self.status_sub_txt.setVisible(False)
            self.available_lbl.setVisible(False)
            self.ready_lbl.setVisible(False)
            self.charger_icon.setText("payments")
            self.status_txt.setText("TRANSACTION" if self.current_lang == "en" else "TRANSAKSI")
            self.status_box.setStyleSheet("""
                QWidget {
                    background-color: #00a572;
                    border: 2px solid rgba(78, 222, 163, 0.5);
                    border-radius: 16px;
                }
            """)
        elif self.status_state == "charging":
            self.status_sub_txt.setVisible(True)
            self.status_sub_txt.setText("CHARGING" if self.current_lang == "en" else "PENGISIAN")
            self.charger_icon.setText("ev_charger")
            self.status_txt.setText("Status")
            self.status_box.setStyleSheet("""
                QWidget {
                    background-color: #00a572;
                    border: 2px solid rgba(78, 222, 163, 0.5);
                    border-radius: 16px;
                }
            """)
        elif self.status_state == "finishing":
            self.status_sub_txt.setVisible(True)
            self.status_sub_txt.setText("Finishing" if self.current_lang == "en" else "Selesai")
            self.available_lbl.setVisible(False)
            self.ready_lbl.setVisible(False)
            self.charger_icon.setText("ev_charger")
            self.status_txt.setText("Status")
            self.status_box.setStyleSheet("""
                QWidget {
                    background-color: #00a572;
                    border: 2px solid rgba(78, 222, 163, 0.5);
                    border-radius: 16px;
                }
            """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Sidebar background (#060e20)
        painter.fillRect(self.rect(), QColor("#060e20"))
        
        # Right border line (#3b494b with 20% opacity)
        painter.setPen(QColor(59, 73, 75, 50))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        
        super().paintEvent(event)
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QPixmap, QColor, QFont
from config import BASE_DIR

class SplashScreen(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        
        # Frameless window, stays on top, translucent background
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set size
        self.resize(500, 600)
        
        # Center on screen
        screen = self.screen()
        if screen:
            geom = screen.geometry()
            self.move((geom.width() - self.width()) // 2, (geom.height() - self.height()) // 2)
            
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Container widget with styled background
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            QWidget#container {
                background-color: #0b1326;
                border: 2px solid rgba(0, 240, 255, 0.2);
                border-radius: 24px;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(24)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo image
        self.logo_label = QLabel()
        logo_pixmap = QPixmap(str(BASE_DIR / "resources" / "icon" / "logoputih-removebg-preview.png"))
        if not logo_pixmap.isNull():
            # Scale logo to fit
            self.logo_label.setPixmap(logo_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent; border: none;")
        
        # Title/Subtitle text
        self.title_label = QLabel("BADAN RISET\nDAN INOVASI NASIONAL")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            background: transparent;
            border: none;
            color: #dbfcff;
            font-family: 'Plus Jakarta Sans';
            font-size: 18px;
            font-weight: bold;
            line-height: 1.4;
        """)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(219, 252, 255, 0.1);
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #00f0ff;
                border-radius: 2px;
            }
        """)
        
        # Info/Status Label
        self.status_label = QLabel("Initializing system...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            background: transparent;
            border: none;
            color: #b9cacb;
            font-family: 'Inter';
            font-size: 11px;
        """)
        
        container_layout.addWidget(self.logo_label)
        container_layout.addWidget(self.title_label)
        container_layout.addStretch()
        container_layout.addWidget(self.status_label)
        container_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.container)
        
        # Animation and timers
        self.progress_val = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(25) # 2.5 seconds total (25ms * 100)
        
    def update_progress(self):
        self.progress_val += 1
        self.progress_bar.setValue(self.progress_val)
        
        if self.progress_val == 20:
            self.status_label.setText("Loading user interfaces...")
        elif self.progress_val == 50:
            self.status_label.setText("Establishing connection to grid...")
        elif self.progress_val == 80:
            self.status_label.setText("Optimizing system performance...")
        elif self.progress_val >= 100:
            self.timer.stop()
            self.fade_out()
            
    def fade_out(self):
        # Window fade-out animation
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.finish_splash)
        self.anim.start()
        
    def finish_splash(self):
        self.close()
        self.callback()

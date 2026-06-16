from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, QRect, QRectF, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QLinearGradient, QPainterPath
from config import BASE_DIR

class LayoutButton(QPushButton):
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


class MarqueeLabel(QWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._full_text = text
        self.offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(25) # ~40 fps
        self.setFixedHeight(30)

    @property
    def full_text(self):
        return self._full_text

    @full_text.setter
    def full_text(self, val):
        self._full_text = val
        self.offset = 0
        self.update()

    def scroll_text(self):
        self.offset -= 0.8
        font = QFont("Inter", 12)
        metrics = self.fontMetrics()
        text_width = metrics.horizontalAdvance(self._full_text)
        if text_width == 0:
            return
        if self.offset < -text_width:
            self.offset = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(QFont("Inter", 12))
        painter.setPen(QColor("#b9cacb"))
        
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(self._full_text)
        if text_width == 0:
            return
            
        y = (self.height() - metrics.height()) // 2 + metrics.ascent()
        
        # Draw repeated text to fill the entire width seamlessly
        x = self.offset
        while x < self.width():
            painter.drawText(int(x), y, self._full_text)
            x += text_width


class BouncingTooltip(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.bounce = 0.0
        self.direction = 1
        self.text = "TAP RFID OR SCREEN TO BEGIN"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(40) # ~25 fps
        
    def animate(self):
        self.bounce += self.direction * 0.4
        if abs(self.bounce) > 6:
            self.direction *= -1
        self.update()

    def update_language(self, lang):
        if lang == "en":
            self.text = "TAP RFID OR SCREEN TO BEGIN"
        else:
            self.text = "TEMPELKAN RFID ATAU LAYAR UNTUK MEMULAI"
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw text
        painter.setFont(QFont("Space Grotesk", 14, QFont.Weight.Bold))
        painter.setPen(QColor(185, 202, 203, 130)) # #b9cacb at 50% opacity
        
        metrics = painter.fontMetrics()
        w = metrics.horizontalAdvance(self.text)
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        
        # Center the text vertically
        text_y = int(cy + metrics.ascent()/2.0 - 2)
        painter.drawText(int(cx - w/2.0), text_y, self.text)
        
        # Bouncing arrows
        painter.setFont(QFont("Material Symbols Outlined", 18))
        arrow_w = painter.fontMetrics().horizontalAdvance("arrow_downward")
        arrow_y = int(cy + painter.fontMetrics().ascent()/2.0 - 4 + self.bounce)
        
        # Left arrow
        painter.drawText(int(cx - w/2.0 - 40 - arrow_w/2.0), arrow_y, "arrow_downward")
        # Right arrow
        painter.drawText(int(cx + w/2.0 + 40 - arrow_w/2.0), arrow_y, "arrow_downward")


class HeroSection(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(str(BASE_DIR / "resources" / "images" / "ev_car.jpg"))
        
        # Layout inside Hero Card
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Top Row: Floating Start Charging Button
        top_row = QHBoxLayout()
        top_row.addStretch()
        
        self.start_btn = LayoutButton()
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #00f0ff;
                border: none;
                border-radius: 26px;
            }
            QPushButton:hover {
                background-color: #00dbe9;
            }
            QPushButton:pressed {
                background-color: #00b8c4;
            }
        """)
        self.start_btn.setFixedHeight(52)
        
        btn_layout = QHBoxLayout(self.start_btn)
        btn_layout.setContentsMargins(28, 0, 28, 0)
        btn_layout.setSpacing(12)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_icon = QLabel("touch_app")
        btn_icon.setFont(QFont("Material Symbols Outlined", 24))
        btn_icon.setStyleSheet("color: #00363a; background: transparent; border: none;")
        
        self.btn_txt = QLabel("START CHARGING")
        self.btn_txt.setFont(QFont("Space Grotesk", 16, QFont.Weight.Bold))
        self.btn_txt.setStyleSheet("color: #00363a; background: transparent; border: none;")
        
        btn_layout.addWidget(btn_icon)
        btn_layout.addWidget(self.btn_txt)
        
        # Glow Effect for Button
        btn_shadow = QGraphicsDropShadowEffect(self.start_btn)
        btn_shadow.setBlurRadius(25)
        btn_shadow.setColor(QColor(0, 240, 255, 120))
        btn_shadow.setOffset(0, 4)
        self.start_btn.setGraphicsEffect(btn_shadow)
        
        top_row.addWidget(self.start_btn)
        layout.addLayout(top_row)
        
        layout.addStretch()
        
        # Bottom Column: Pill Badge, Title, Description
        bottom_col = QVBoxLayout()
        bottom_col.setSpacing(14)
        
        # Pill Badge (Global Network)
        self.pill = QWidget()
        self.pill.setStyleSheet("""
            QWidget {
                background-color: rgba(78, 222, 163, 0.15);
                border: 1px solid rgba(78, 222, 163, 0.3);
                border-radius: 14px;
            }
        """)
        self.pill.setFixedHeight(28)
        
        pill_layout = QHBoxLayout(self.pill)
        pill_layout.setContentsMargins(12, 0, 12, 0)
        pill_layout.setSpacing(8)
        pill_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Pulse Dot inside Pill
        self.dot = QLabel("●")
        self.dot.setFont(QFont("Inter", 8))
        self.dot.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        
        self.pill_txt = QLabel("GLOBAL NETWORK")
        self.pill_txt.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        self.pill_txt.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 1.5px;")
        
        pill_layout.addWidget(self.dot)
        pill_layout.addWidget(self.pill_txt)
        
        # Pulse dot animation
        self.dot_opacity = 1.0
        self.dot_dir = -1
        self.dot_timer = QTimer(self)
        self.dot_timer.timeout.connect(self.pulse_dot)
        self.dot_timer.start(100)
        
        # Title Label
        self.title_lbl = QLabel("Powering the\nFuture of Mobility")
        self.title_lbl.setFont(QFont("Space Grotesk", 36, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #dbfcff; background: transparent;")
        self.title_lbl.setWordWrap(True)
        
        # Description Label
        self.desc_lbl = QLabel("Experience 350kW ultra-fast charging. Seamless, sustainable, and smarter than ever before.")
        self.desc_lbl.setFont(QFont("Inter", 14))
        self.desc_lbl.setStyleSheet("color: #b9cacb; background: transparent;")
        self.desc_lbl.setWordWrap(True)
        
        bottom_col.addWidget(self.pill, 0, Qt.AlignmentFlag.AlignLeft)
        bottom_col.addWidget(self.title_lbl)
        bottom_col.addWidget(self.desc_lbl)
        
        layout.addLayout(bottom_col)

    def pulse_dot(self):
        self.dot_opacity += self.dot_dir * 0.1
        if self.dot_opacity <= 0.3:
            self.dot_opacity = 0.3
            self.dot_dir = 1
        elif self.dot_opacity >= 1.0:
            self.dot_opacity = 1.0
            self.dot_dir = -1
        # Set stylesheet with updated alpha
        alpha = int(self.dot_opacity * 255)
        self.dot.setStyleSheet(f"color: rgba(78, 222, 163, {alpha}); background: transparent; border: none;")

    def update_language(self, lang):
        if lang == "en":
            self.pill_txt.setText("GLOBAL NETWORK")
            self.btn_txt.setText("START CHARGING")
            self.title_lbl.setText("Powering the\nFuture of Mobility")
            self.desc_lbl.setText("Experience 350kW ultra-fast charging. Seamless, sustainable, and smarter than ever before.")
        else: # id
            self.pill_txt.setText("JARINGAN GLOBAL")
            self.btn_txt.setText("MULAI PENGISIAN")
            self.title_lbl.setText("Mendorong Masa\nDepan Mobilitas")
            self.desc_lbl.setText("Rasakan pengisian daya ultra-cepat 350kW. Mulus, berkelanjutan, dan lebih pintar dari sebelumnya.")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # 1. Rounded Clip Path
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 24.0, 24.0)
        painter.setClipPath(path)
        
        # 2. Draw Cover Image
        if not self.pixmap.isNull():
            img_w = self.pixmap.width()
            img_h = self.pixmap.height()
            rect_w = rect.width()
            rect_h = rect.height()
            
            img_ratio = img_w / img_h
            rect_ratio = rect_w / rect_h
            
            if img_ratio > rect_ratio:
                src_h = img_h
                src_w = int(img_h * rect_ratio)
                src_x = int((img_w - src_w) / 2)
                src_y = 0
            else:
                src_w = img_w
                src_h = int(img_w / rect_ratio)
                src_x = 0
                src_y = int((img_h - src_h) / 2)
                
            painter.drawPixmap(rect, self.pixmap, QRect(src_x, src_y, src_w, src_h))
            
        # 3. Overlay bottom-up dark gradient
        gradient = QLinearGradient(0, rect.bottom(), 0, rect.top())
        gradient.setColorAt(0, QColor(11, 19, 38, 235)) # Dark background base
        gradient.setColorAt(0.5, QColor(11, 19, 38, 120))
        gradient.setColorAt(1, QColor(11, 19, 38, 10))
        painter.fillRect(rect, gradient)


class IdleState(QWidget):
    start_charging_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.ticker_text_en = " • Station 4882-X: Full compatibility with all CSS standard models • Energy sourced 100% from solar array 04 • Welcome to VOLTCORE - Ultra Fast EV Charging Network • Special rate of $0.25/kWh until midnight • Download the VOLTCORE app for loyalty rewards •"
        self.ticker_text_id = " • Stasiun 4882-X: Kompatibilitas penuh dengan semua model standar CSS • Energi bersumber 100% dari panel surya 04 • Selamat datang di VOLTCORE - Jaringan Pengisian Daya EV Ultra Cepat • Tarif khusus Rp 4.000/kWh hingga tengah malam • Unduh aplikasi VOLTCORE untuk hadiah loyalitas •"

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 48, 48, 20)
        layout.setSpacing(28)

        # Hero Card
        self.hero = HeroSection()
        self.hero.start_btn.clicked.connect(self.start_charging_clicked.emit)
        layout.addWidget(self.hero, 1) # Expand hero card to fill vertical space

        # Bottom Row: 3 visual widgets
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # Card 1: Grid Efficiency
        self.grid_card = QWidget()
        self.grid_card.setFixedHeight(96)
        self.grid_card.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 52, 73, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }
        """)
        
        grid_layout = QHBoxLayout(self.grid_card)
        grid_layout.setContentsMargins(20, 0, 20, 0)
        grid_layout.setSpacing(16)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        icon_box = QWidget()
        icon_box.setFixedSize(52, 52)
        icon_box.setStyleSheet("""
            QWidget {
                background-color: #222a3d;
                border: none;
                border-radius: 10px;
            }
        """)
        icon_box_layout = QVBoxLayout(icon_box)
        icon_box_layout.setContentsMargins(0, 0, 0, 0)
        icon_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        bolt_icon = QLabel("bolt")
        bolt_icon.setFont(QFont("Material Symbols Outlined", 30))
        bolt_icon.setStyleSheet("color: #4edea3; background: transparent;")
        bolt_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box_layout.addWidget(bolt_icon)

        grid_text_layout = QVBoxLayout()
        grid_text_layout.setSpacing(2)
        grid_text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.grid_lbl = QLabel("GRID EFFICIENCY")
        self.grid_lbl.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        self.grid_lbl.setStyleSheet("color: #b9cacb; opacity: 0.6; background: transparent; border: none; letter-spacing: 1px;")
        
        grid_val = QLabel("98.4%")
        grid_val.setFont(QFont("Space Grotesk", 24, QFont.Weight.Bold))
        grid_val.setStyleSheet("color: #dbfcff; background: transparent; border: none;")

        grid_text_layout.addWidget(self.grid_lbl)
        grid_text_layout.addWidget(grid_val)

        grid_layout.addWidget(icon_box)
        grid_layout.addLayout(grid_text_layout)
        grid_layout.addStretch()

        # Card 2: Live Updates (Ticker)
        self.updates_card = QWidget()
        self.updates_card.setFixedHeight(96)
        self.updates_card.setStyleSheet("""
            QWidget {
                background-color: rgba(6, 14, 32, 0.45);
                border: 1px solid rgba(59, 73, 75, 0.15);
                border-radius: 16px;
            }
        """)
        
        updates_layout = QVBoxLayout(self.updates_card)
        updates_layout.setContentsMargins(20, 14, 20, 14)
        updates_layout.setSpacing(6)

        updates_header = QHBoxLayout()
        updates_header.setSpacing(8)
        updates_header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        info_icon = QLabel("info")
        info_icon.setFont(QFont("Material Symbols Outlined", 16))
        info_icon.setStyleSheet("color: #00dbe9; background: transparent; border: none;")
        
        self.updates_lbl = QLabel("LIVE UPDATES")
        self.updates_lbl.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        self.updates_lbl.setStyleSheet("color: #00dbe9; background: transparent; border: none; letter-spacing: 1.5px;")

        updates_header.addWidget(info_icon)
        updates_header.addWidget(self.updates_lbl)

        self.ticker = MarqueeLabel(self.ticker_text_en)

        updates_layout.addLayout(updates_header)
        updates_layout.addWidget(self.ticker)

        # Card 3: Weather
        self.weather_card = QWidget()
        self.weather_card.setFixedHeight(96)
        self.weather_card.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 52, 73, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }
        """)
        
        weather_layout = QHBoxLayout(self.weather_card)
        weather_layout.setContentsMargins(20, 0, 20, 0)
        weather_layout.setSpacing(16)
        weather_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        weather_text_layout = QVBoxLayout()
        weather_text_layout.setSpacing(2)
        weather_text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        temp_lbl = QLabel("24°C")
        temp_lbl.setFont(QFont("Plus Jakarta Sans", 24, QFont.Weight.Bold))
        temp_lbl.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        self.weather_lbl = QLabel("Sunny")
        self.weather_lbl.setFont(QFont("Inter", 12))
        self.weather_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")

        weather_text_layout.addWidget(temp_lbl)
        weather_text_layout.addWidget(self.weather_lbl)

        sun_icon = QLabel("wb_sunny")
        sun_icon.setFont(QFont("Material Symbols Outlined", 36))
        sun_icon.setStyleSheet("color: #adc6ff; background: transparent; border: none;")
        sun_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        weather_layout.addLayout(weather_text_layout)
        weather_layout.addStretch()
        weather_layout.addWidget(sun_icon)

        # Add cards to bottom row with proportional widths (Grid: 1.2, Ticker: 2.2, Weather: 1.0)
        bottom_row.addWidget(self.grid_card, 12)
        bottom_row.addWidget(self.updates_card, 22)
        bottom_row.addWidget(self.weather_card, 10)

        layout.addLayout(bottom_row)

        # Bouncing Tooltip at the very bottom
        self.tooltip = BouncingTooltip()
        layout.addWidget(self.tooltip)

    def update_language(self, lang):
        # Update Hero Section
        self.hero.update_language(lang)
        # Update Bouncing Tooltip
        self.tooltip.update_language(lang)
        # Update Cards Labels
        if lang == "en":
            self.grid_lbl.setText("GRID EFFICIENCY")
            self.updates_lbl.setText("LIVE UPDATES")
            self.weather_lbl.setText("Sunny")
            self.ticker.full_text = self.ticker_text_en
        else: # id
            self.grid_lbl.setText("EFISIENSI JARINGAN")
            self.updates_lbl.setText("INFORMASI TERKINI")
            self.weather_lbl.setText("Cerah")
            self.ticker.full_text = self.ticker_text_id

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Draw base background
        painter.fillRect(rect, QColor("#0b1326"))
        
        # Draw RFID scanner subtle cyan glow in bottom-right corner
        from PyQt6.QtGui import QRadialGradient
        glow = QRadialGradient(float(rect.width()), float(rect.height()), float(min(rect.width(), rect.height())) * 0.4)
        glow.setColorAt(0.0, QColor(0, 240, 255, 30))  # Light cyan with 12% opacity
        glow.setColorAt(0.5, QColor(0, 240, 255, 10))
        glow.setColorAt(1.0, Qt.GlobalColor.transparent)
        painter.fillRect(rect, glow)
        
        super().paintEvent(event)
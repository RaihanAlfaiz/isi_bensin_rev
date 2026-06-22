from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, QRect, QRectF, QPropertyAnimation, pyqtSignal, QTime
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


class LastTxBentoCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(110)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 52, 73, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }
        """)
        self.current_lang = "en"
        self.session_data = {
            "date": "18 Jun 2026",
            "time": "14:35 WIB",
            "soc": "85%",
            "energy": "20.4 kWh",
            "duration": "01:35:12",
            "cost": "Rp 51.000"
        }
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 10, 16, 10)
        main_layout.setSpacing(6)
        
        header = QHBoxLayout()
        header.setSpacing(6)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        icon = QLabel("history")
        icon.setFont(QFont("Material Symbols Outlined", 14))
        icon.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        
        self.title_lbl = QLabel("LAST TRANSACTION")
        self.title_lbl.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #4edea3; background: transparent; border: none; letter-spacing: 1px;")
        
        header.addWidget(icon)
        header.addWidget(self.title_lbl)
        main_layout.addLayout(header)
        
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent; border: none;")
        self.grid = QGridLayout(grid_widget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(2)
        
        self.lbl_date = QLabel("Date:")
        self.val_date = QLabel()
        self.lbl_time = QLabel("Time:")
        self.val_time = QLabel()
        self.lbl_soc = QLabel("Final SOC:")
        self.val_soc = QLabel()
        
        self.lbl_energy = QLabel("Energy:")
        self.val_energy = QLabel()
        self.lbl_dur = QLabel("Duration:")
        self.val_dur = QLabel()
        self.lbl_cost = QLabel("Cost:")
        self.val_cost = QLabel()
        
        label_style = "color: #b9cacb; opacity: 0.7; background: transparent; border: none;"
        value_style = "color: #ffffff; background: transparent; border: none; font-weight: bold;"
        
        for lbl in [self.lbl_date, self.lbl_time, self.lbl_soc, self.lbl_energy, self.lbl_dur, self.lbl_cost]:
            lbl.setFont(QFont("Inter", 9))
            lbl.setStyleSheet(label_style)
            
        for val in [self.val_date, self.val_time, self.val_soc, self.val_energy, self.val_dur, self.val_cost]:
            val.setFont(QFont("Space Grotesk", 9))
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
        
        main_layout.addWidget(grid_widget)
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
            self.lbl_soc.setText("Final SOC:")
            self.lbl_energy.setText("Energy:")
            self.lbl_dur.setText("Duration:")
            self.lbl_cost.setText("Cost:")
        else:
            self.title_lbl.setText("TRANSAKSI TERAKHIR")
            self.lbl_date.setText("Tanggal:")
            self.lbl_time.setText("Waktu:")
            self.lbl_soc.setText("Final SOC:")
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


class LiveUpdatesFeed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        self.events = [
            {
                "time": "14:30",
                "text_en": "Reserved Session Created",
                "text_id": "Sesi Reservasi Dibuat",
                "icon": "bookmark",
                "color": "#ffaa44"
            },
            {
                "time": "14:35",
                "text_en": "Queue Updated (2 waiting)",
                "text_id": "Antrean Diperbarui (2 menunggu)",
                "icon": "people",
                "color": "#00dbe9"
            }
        ]
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        
        self.refresh_display()
        
    def add_event(self, time_str, text_en, text_id, icon, color):
        self.events.insert(0, {
            "time": time_str,
            "text_en": text_en,
            "text_id": text_id,
            "icon": icon,
            "color": color
        })
        if len(self.events) > 2:
            self.events = self.events[:2]
        self.refresh_display()
        
    def update_language(self, lang):
        self.current_lang = lang
        self.refresh_display()
        
    def refresh_display(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        for event in self.events:
            event_widget = QWidget()
            event_widget.setStyleSheet("background: transparent; border: none;")
            h_layout = QHBoxLayout(event_widget)
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.setSpacing(8)
            
            icon_lbl = QLabel(event["icon"])
            icon_lbl.setFont(QFont("Material Symbols Outlined", 14))
            icon_lbl.setStyleSheet(f"color: {event['color']}; background: transparent; border: none;")
            
            time_lbl = QLabel(f"[{event['time']}]")
            time_lbl.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
            time_lbl.setStyleSheet("color: rgba(255, 255, 255, 0.4); background: transparent; border: none;")
            
            text_str = event["text_en"] if self.current_lang == "en" else event["text_id"]
            text_lbl = QLabel(text_str)
            text_lbl.setFont(QFont("Inter", 10))
            text_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
            text_lbl.setWordWrap(True)
            
            h_layout.addWidget(icon_lbl)
            h_layout.addWidget(time_lbl)
            h_layout.addWidget(text_lbl, 1)
            
            self.layout.addWidget(event_widget)


class IdleState(QWidget):
    start_charging_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()

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

        # Card 1: Last Transaction
        self.last_tx_card = LastTxBentoCard()

        # Card 2: Live Updates
        self.updates_card = QWidget()
        self.updates_card.setFixedHeight(110)
        self.updates_card.setStyleSheet("""
            QWidget {
                background-color: rgba(6, 14, 32, 0.45);
                border: 1px solid rgba(59, 73, 75, 0.15);
                border-radius: 16px;
            }
        """)
        
        updates_layout = QVBoxLayout(self.updates_card)
        updates_layout.setContentsMargins(20, 12, 20, 12)
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

        self.feed = LiveUpdatesFeed()

        updates_layout.addLayout(updates_header)
        updates_layout.addWidget(self.feed)

        # Card 3: Weather
        self.weather_card = QWidget()
        self.weather_card.setFixedHeight(110)
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

        # Add cards to bottom row with proportional widths (LastTx: 20, Ticker: 28, Weather: 16)
        bottom_row.addWidget(self.last_tx_card, 20)
        bottom_row.addWidget(self.updates_card, 28)
        bottom_row.addWidget(self.weather_card, 16)

        layout.addLayout(bottom_row)

    def add_system_event(self, text_en, text_id, icon="info", color="#00dbe9"):
        time_str = QTime.currentTime().toString("HH:mm")
        self.feed.add_event(time_str, text_en, text_id, icon, color)

    def update_language(self, lang):
        # Update Hero Section
        self.hero.update_language(lang)
        # Update Last Transaction Card
        self.last_tx_card.update_language(lang)
        # Update Feed Language
        self.feed.update_language(lang)
        # Update Cards Labels
        if lang == "en":
            self.updates_lbl.setText("LIVE UPDATES")
            self.weather_lbl.setText("Sunny")
        else: # id
            self.updates_lbl.setText("INFORMASI TERKINI")
            self.weather_lbl.setText("Cerah")

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
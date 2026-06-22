from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QGraphicsDropShadowEffect, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QTimer, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QRadialGradient
import random
import math

class ChargingGauge(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(340, 340)
        self.percentage = 78
        self.kw = 120.4
        self.glow_phase = 0.0
        
        # Layout for centered texts
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)
        
        # Percentage Label
        self.pct_layout = QHBoxLayout()
        self.pct_layout.setSpacing(0)
        self.pct_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.pct_val = QLabel("78")
        self.pct_val.setFont(QFont("Plus Jakarta Sans", 64, QFont.Weight.Bold))
        self.pct_val.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        
        self.pct_symbol = QLabel("%")
        self.pct_symbol.setFont(QFont("Plus Jakarta Sans", 24, QFont.Weight.Bold))
        self.pct_symbol.setStyleSheet("color: #4edea3; opacity: 0.7; background: transparent; border: none; margin-bottom: 16px;")
        
        self.pct_layout.addWidget(self.pct_val)
        self.pct_layout.addWidget(self.pct_symbol)
        
        # Label Title
        self.title_lbl = QLabel("POWER LEVEL")
        self.title_lbl.setFont(QFont("Space Grotesk", 12, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #dbfcff; opacity: 0.8; background: transparent; border: none; letter-spacing: 2px;")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # KW Row
        self.kw_layout = QHBoxLayout()
        self.kw_layout.setSpacing(8)
        self.kw_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.bolt_icon = QLabel("bolt")
        self.bolt_icon.setFont(QFont("Material Symbols Outlined", 22))
        self.bolt_icon.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        
        self.kw_val = QLabel("120.4")
        self.kw_val.setFont(QFont("Space Grotesk", 18, QFont.Weight.Bold))
        self.kw_val.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        self.kw_unit = QLabel("kW")
        self.kw_unit.setFont(QFont("Space Grotesk", 12, QFont.Weight.Bold))
        self.kw_unit.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        self.kw_layout.addWidget(self.bolt_icon)
        self.kw_layout.addWidget(self.kw_val)
        self.kw_layout.addWidget(self.kw_unit)
        
        layout.addLayout(self.pct_layout)
        layout.addWidget(self.title_lbl)
        layout.addLayout(self.kw_layout)
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30) # ~33 fps for glowing effects
        
        self.bolt_timer = QTimer(self)
        self.bolt_timer.timeout.connect(self.toggle_bolt)
        self.bolt_timer.start(1000)
        self.bolt_visible = True
        
    def animate(self):
        # Pulse glow effect phase
        self.glow_phase += 0.05
        if self.glow_phase >= 2 * math.pi:
            self.glow_phase = 0.0
        self.update()
        
    def toggle_bolt(self):
        self.bolt_visible = not self.bolt_visible
        if self.bolt_visible:
            self.bolt_icon.setStyleSheet("color: #4edea3; background: transparent; border: none;")
        else:
            self.bolt_icon.setStyleSheet("color: rgba(78, 222, 163, 0.3); background: transparent; border: none;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        size = min(w, h) - 40
        rect = QRectF((w - size) / 2.0, (h - size) / 2.0, size, size)
        
        # Background ring (track)
        bg_pen = QPen(QColor(255, 255, 255, 12), 10)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(rect)
        
        # Draw pulsing outer neon glow
        glow_alpha = int(40 + 20 * math.sin(self.glow_phase))
        glow_pen = QPen(QColor(78, 222, 163, glow_alpha), 22)
        painter.setPen(glow_pen)
        start_angle = 90 * 16
        span_angle = -int((self.percentage / 100.0) * 360.0) * 16
        painter.drawArc(rect, start_angle, span_angle)
        
        # Active progress arc
        active_pen = QPen(QColor(78, 222, 163), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(active_pen)
        painter.drawArc(rect, start_angle, span_angle)
        
        super().paintEvent(event)


class StatsCard(QWidget):
    def __init__(self, icon_str, title_str, val_str, unit_str="", parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumHeight(110)
        
        self.setStyleSheet("""
            StatsCard {
                background: rgba(23, 31, 51, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Header Row
        header = QHBoxLayout()
        header.setSpacing(8)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.icon_lbl = QLabel(icon_str)
        self.icon_lbl.setFont(QFont("Material Symbols Outlined", 18))
        self.icon_lbl.setStyleSheet("color: #dbfcff; opacity: 0.6; background: transparent; border: none;")
        
        self.title_lbl = QLabel(title_str)
        self.title_lbl.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #dbfcff; opacity: 0.6; background: transparent; border: none; letter-spacing: 1px; line-height: 1.2;")
        self.title_lbl.setWordWrap(True)
        
        header.addWidget(self.icon_lbl)
        header.addWidget(self.title_lbl, 1)
        
        # Value Row
        self.val_layout = QHBoxLayout()
        self.val_layout.setSpacing(6)
        self.val_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        
        self.val_lbl = QLabel(val_str)
        self.val_lbl.setFont(QFont("Space Grotesk", 28, QFont.Weight.Bold))
        self.val_lbl.setStyleSheet("color: #dae2fd; background: transparent; border: none;")
        
        self.unit_lbl = QLabel(unit_str)
        self.unit_lbl.setFont(QFont("Inter", 13))
        self.unit_lbl.setStyleSheet("color: #b9cacb; opacity: 0.6; background: transparent; border: none; margin-bottom: 4px;")
        
        self.val_layout.addWidget(self.val_lbl)
        if unit_str:
            self.val_layout.addWidget(self.unit_lbl)
            
        layout.addLayout(header)
        layout.addLayout(self.val_layout)


class ChargingState(QWidget):
    charging_completed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "en"
        self.seconds_elapsed = 1275 # Start from 21:15 like HTML
        self.energy_delivered = 5.6
        self.target_percentage = 100
        
        self.setup_ui()
        self.update_language("en")
        
        # Simulation timer
        self.sim_timer = QTimer(self)
        self.sim_timer.timeout.connect(self.run_simulation)
        
    def showEvent(self, event):
        super().showEvent(event)
        # Reset simulation variables when entering page
        self.seconds_elapsed = 1275
        self.energy_delivered = 5.6
        self.gauge.percentage = 78
        target_kw = getattr(self, "max_power_kw", 120.4)
        self.gauge.kw = target_kw
        self.gauge.pct_val.setText("78")
        self.gauge.kw_val.setText(f"{self.gauge.kw:.1f}")
        self.update_timer_label()
        self.update_energy_label()
        self.sim_timer.start(1000) # Update every 1 second
        
    def hideEvent(self, event):
        self.sim_timer.stop()
        super().hideEvent(event)
        
    def run_simulation(self):
        self.seconds_elapsed += 1
        self.update_timer_label()
        
        # Fluctuate kW rate around max_power_kw
        target_kw = getattr(self, "max_power_kw", 120.4)
        fluq = random.uniform(-target_kw * 0.005, target_kw * 0.005) # +/- 0.5%
        self.gauge.kw = max(target_kw * 0.95, min(target_kw * 1.05, self.gauge.kw + fluq))
        self.gauge.kw_val.setText(f"{self.gauge.kw:.1f}")
        
        # Accumulate energy delivered
        self.energy_delivered += (self.gauge.kw / 3600.0)
        self.update_energy_label()
        
        # Accumulate percentage
        # Let's say it increases 1% every 3 seconds for a responsive visualization
        if self.seconds_elapsed % 3 == 0:
            if self.gauge.percentage < self.target_percentage:
                self.gauge.percentage += 1
                self.gauge.pct_val.setText(str(self.gauge.percentage))
                
                # Check for completion
                if self.gauge.percentage >= self.target_percentage:
                    self.finish_charging()
                    
    def finish_charging(self):
        self.sim_timer.stop()
        # Trigger completed signal to go back to Idle
        self.charging_completed.emit()
        
    def update_timer_label(self):
        h = self.seconds_elapsed // 3600
        m = (self.seconds_elapsed % 3600) // 60
        s = self.seconds_elapsed % 60
        self.time_card.val_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")
        
    def update_energy_label(self):
        self.energy_card.val_lbl.setText(f"{self.energy_delivered:.1f}")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 20)
        layout.setSpacing(0)
        
        # Spacer at top to push everything down slightly and distribute space
        layout.addStretch(1)
        
        # 1. Main Animated Circular Gauge (Top)
        self.gauge = ChargingGauge()
        self.gauge.clicked.connect(self.finish_charging)
        layout.addWidget(self.gauge, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Spacing between Gauge and Title
        layout.addSpacing(24)
        
        # 2. Title Section (Middle)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.header_title = QLabel("Active Power Flow")
        self.header_title.setFont(QFont("Plus Jakarta Sans", 28, QFont.Weight.Bold))
        self.header_title.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        self.header_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.header_sub = QLabel("Hyper-Fast Charging Engaged")
        self.header_sub.setFont(QFont("Inter", 13))
        self.header_sub.setStyleSheet("color: #b9cacb; opacity: 0.7; background: transparent; border: none;")
        self.header_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(self.header_title)
        title_layout.addWidget(self.header_sub)
        
        layout.addLayout(title_layout)
        
        # Spacing between Title and Stats
        layout.addSpacing(32)
        
        # 3. Stats Bento grid row (Bottom)
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(20)
        
        self.time_card = StatsCard("schedule", "CHARGING TIME", "00:21:15")
        self.energy_card = StatsCard("electric_car", "ENERGY\nDELIVERED", "5.6", "kWh")
        self.comp_card = StatsCard("battery_charging_full", "EST. COMPLETION", "12:45", "PM")
        
        self.stats_row.addWidget(self.time_card)
        self.stats_row.addWidget(self.energy_card)
        self.stats_row.addWidget(self.comp_card)
        layout.addLayout(self.stats_row)
        
        # Spacer before the stop button row
        layout.addStretch(1)
        
        # 4. Emergency Stop Trigger
        self.stop_btn = QPushButton()
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.clicked.connect(self.finish_charging)
        self.stop_btn.setStyleSheet("background: transparent; border: none;")
        
        stop_layout = QHBoxLayout(self.stop_btn)
        stop_layout.setSpacing(12)
        stop_layout.setContentsMargins(0, 0, 0, 0)
        
        text_stop_layout = QVBoxLayout()
        text_stop_layout.setSpacing(2)
        text_stop_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.stop_title = QLabel("EMERGENCY STOP")
        self.stop_title.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        self.stop_title.setStyleSheet("color: #ffb4ab; background: transparent; border: none;")
        self.stop_title.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.stop_desc = QLabel("Push physical button below")
        self.stop_desc.setFont(QFont("Inter", 8))
        self.stop_desc.setStyleSheet("color: #b9cacb; opacity: 0.6; background: transparent; border: none;")
        self.stop_desc.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        text_stop_layout.addWidget(self.stop_title)
        text_stop_layout.addWidget(self.stop_desc)
        
        # Pulse stop indicator
        self.stop_pulse = QWidget()
        self.stop_pulse.setFixedSize(32, 32)
        self.stop_pulse.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 180, 171, 0.2);
                border: 2px solid #ffb4ab;
                border-radius: 16px;
            }
        """)
        
        stop_layout.addLayout(text_stop_layout)
        stop_layout.addWidget(self.stop_pulse)
        
        self.stop_btn.setFixedHeight(45)
        self.stop_btn.setFixedWidth(240)
        
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        bottom_row.addWidget(self.stop_btn)
        
        layout.addLayout(bottom_row)
        
    def update_language(self, lang):
        self.current_lang = lang
        if lang == "en":
            self.header_title.setText("Active Power Flow")
            self.header_sub.setText("Hyper-Fast Charging Engaged")
            self.time_card.title_lbl.setText("CHARGING TIME")
            self.energy_card.title_lbl.setText("ENERGY\nDELIVERED")
            self.comp_card.title_lbl.setText("EST. COMPLETION")
            self.comp_card.unit_lbl.setText("PM")
            self.stop_title.setText("EMERGENCY STOP")
            self.stop_desc.setText("Push physical button below")
            self.gauge.title_lbl.setText("POWER LEVEL")
        else: # id
            self.header_title.setText("Aliran Daya Aktif")
            self.header_sub.setText("Pengisian Daya Sangat Cepat Aktif")
            self.time_card.title_lbl.setText("WAKTU PENGISIAN")
            self.energy_card.title_lbl.setText("ENERGI\nDIALIRKAN")
            self.comp_card.title_lbl.setText("ESTIMASI SELESAI")
            self.comp_card.unit_lbl.setText("SIANG")
            self.stop_title.setText("PEMBERHENTIAN DARURAT")
            self.stop_desc.setText("Tekan tombol fisik di bawah")
            self.gauge.title_lbl.setText("TINGKAT DAYA")
            
    def set_power_limit(self, max_power_kw):
        self.max_power_kw = max_power_kw
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        painter.fillRect(rect, QColor("#0b1326"))
        
        # Radial background gradient
        from PyQt6.QtGui import QRadialGradient
        glow = QRadialGradient(float(rect.width()/2.0), float(rect.height()/2.0), float(min(rect.width(), rect.height())) * 0.7)
        glow.setColorAt(0.0, QColor(78, 222, 163, 12))  # green charging glow
        glow.setColorAt(0.5, QColor(0, 240, 255, 4))
        glow.setColorAt(1.0, Qt.GlobalColor.transparent)
        painter.fillRect(rect, glow)
        
        super().paintEvent(event)

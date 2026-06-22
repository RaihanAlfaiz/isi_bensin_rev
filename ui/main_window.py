from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFontDatabase
from ui.widgets.sidebar import Sidebar
from pages.idle_state import IdleState
from pages.plug_in_state import PlugInState
from pages.payment_state import PaymentState
from pages.charging_state import ChargingState
from pages.finishing_state import FinishingState
from config import BASE_DIR

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load fonts
        self.load_fonts()
        
        self.setWindowTitle("VOLTCORE - Idle State")
        self.resize(1024, 768)  # standard kiosk resolution or nice widescreen proportion
        self.setMinimumSize(960, 640)

        # Style central widget background
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        central_widget.setStyleSheet("QWidget#central_widget { background-color: #0b1326; }")
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.station_id = "4882-X"
        self.max_power_kw = 350
        self.price_per_kwh = 2500
        self.sidebar.set_station_id(self.station_id)
        
        self.stacked_widget = QStackedWidget()
        self.idle_page = IdleState()
        self.plugin_page = PlugInState()
        self.payment_page = PaymentState()
        self.charging_page = ChargingState()
        self.finishing_page = FinishingState()
        
        self.stacked_widget.addWidget(self.idle_page)
        self.stacked_widget.addWidget(self.plugin_page)
        self.stacked_widget.addWidget(self.payment_page)
        self.stacked_widget.addWidget(self.charging_page)
        self.stacked_widget.addWidget(self.finishing_page)

        # Session data initialization
        self.last_session_details = {
            "date": "18 Jun 2026",
            "time": "14:35 WIB",
            "soc": "85%",
            "energy": "20.4 kWh",
            "duration": "01:35:12",
            "cost": "Rp 51.000"
        }
        
        # Sync initial session data
        self.sidebar.update_last_transaction(
            self.last_session_details["date"],
            self.last_session_details["time"],
            self.last_session_details["soc"],
            self.last_session_details["energy"],
            self.last_session_details["duration"],
            self.last_session_details["cost"]
        )
        self.idle_page.last_tx_card.update_session(
            self.last_session_details["date"],
            self.last_session_details["time"],
            self.last_session_details["soc"],
            self.last_session_details["energy"],
            self.last_session_details["duration"],
            self.last_session_details["cost"]
        )

        # Connect signals
        self.sidebar.language_changed.connect(self.on_language_changed)
        self.sidebar.settings_btn.clicked.connect(self.open_settings_dialog)
        self.idle_page.start_charging_clicked.connect(self.on_start_charging)
        self.plugin_page.proceed_to_payment.connect(self.on_proceed_to_payment)
        self.payment_page.payment_completed.connect(self.on_payment_completed)
        self.charging_page.charging_completed.connect(self.on_charging_completed)
        self.finishing_page.finish_clicked.connect(self.on_finish_transaction)

        # Add to layout with stretch factors for 20% / 80% proportion
        layout.addWidget(self.sidebar, 2)
        layout.addWidget(self.stacked_widget, 8)

    def open_settings_dialog(self):
        from ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec()

    def set_system_status(self, state):
        self.sidebar.set_status_state(state)
        # Switch pages based on state
        if state in ["idle", "available"]:
            self.stacked_widget.setCurrentWidget(self.idle_page)
        elif state == "preparing":
            self.stacked_widget.setCurrentWidget(self.plugin_page)
        elif state == "charging":
            self.stacked_widget.setCurrentWidget(self.charging_page)
        elif state == "finishing":
            self.stacked_widget.setCurrentWidget(self.finishing_page)
        elif state in ["reserved", "scheduled", "faulted"]:
            self.stacked_widget.setCurrentWidget(self.idle_page)

    def on_language_changed(self, lang):
        # Update all sidebar and main content views
        self.sidebar.update_language(lang)
        self.idle_page.update_language(lang)
        self.plugin_page.update_language(lang)
        self.payment_page.update_language(lang)
        self.charging_page.update_language(lang)
        self.finishing_page.update_language(lang)

    def on_start_charging(self):
        # Switch sidebar status view to preparing mode
        self.sidebar.set_status_state("preparing")
        # Add system event
        self.idle_page.add_system_event(
            "Vehicle Connected",
            "Kendaraan Terhubung",
            icon="link",
            color="#4edea3"
        )
        # Align page translation with currently active language
        self.plugin_page.update_language(self.sidebar.current_lang)
        # Show plugin/video page
        self.stacked_widget.setCurrentWidget(self.plugin_page)

    def on_proceed_to_payment(self):
        # Switch sidebar status view to transaction mode
        self.sidebar.set_status_state("transaction")
        # Align page translation
        self.payment_page.update_language(self.sidebar.current_lang)
        # Show payment page
        self.stacked_widget.setCurrentWidget(self.payment_page)

    def on_payment_completed(self):
        # Switch sidebar status view to charging mode
        self.sidebar.set_status_state("charging")
        # Add system event
        self.idle_page.add_system_event(
            "Charging Started",
            "Pengisian Dimulai",
            icon="bolt",
            color="#00f0ff"
        )
        # Pass power limit to page
        self.charging_page.set_power_limit(self.max_power_kw)
        # Align page translation
        self.charging_page.update_language(self.sidebar.current_lang)
        # Show charging status page
        self.stacked_widget.setCurrentWidget(self.charging_page)

    def on_charging_completed(self):
        # Switch sidebar status view to finishing mode
        self.sidebar.set_status_state("finishing")
        
        # Calculate cost and format session details
        energy = self.charging_page.energy_delivered
        duration_sec = self.charging_page.seconds_elapsed
        cost_val = int(energy * self.price_per_kwh)
        cost_formatted = f"Rp {cost_val:,}".replace(",", ".")
        
        h = duration_sec // 3600
        m = (duration_sec % 3600) // 60
        s = duration_sec % 60
        duration_formatted = f"{h:02d}:{m:02d}:{s:02d}"
        
        current_dt = QDateTime.currentDateTime()
        date_str = current_dt.toString("dd MMM yyyy")
        time_str = current_dt.toString("HH:mm") + " WIB"
        
        self.last_session_details = {
            "date": date_str,
            "time": time_str,
            "soc": "100%",
            "energy": f"{energy:.1f} kWh",
            "duration": duration_formatted,
            "cost": cost_formatted
        }
        
        # Update last transaction info on both widgets
        self.idle_page.last_tx_card.update_session(
            self.last_session_details["date"],
            self.last_session_details["time"],
            self.last_session_details["soc"],
            self.last_session_details["energy"],
            self.last_session_details["duration"],
            self.last_session_details["cost"]
        )
        self.sidebar.update_last_transaction(
            self.last_session_details["date"],
            self.last_session_details["time"],
            self.last_session_details["soc"],
            self.last_session_details["energy"],
            self.last_session_details["duration"],
            self.last_session_details["cost"]
        )
        
        # Add system event
        self.idle_page.add_system_event(
            "Charging Finished",
            "Pengisian Selesai",
            icon="check_circle",
            color="#b57cff"
        )
        
        # Pass variables to finishing page
        self.finishing_page.set_session_details(
            duration_sec,
            energy,
            self.price_per_kwh
        )
        # Align page translation
        self.finishing_page.update_language(self.sidebar.current_lang)
        # Show finishing / summary page
        self.stacked_widget.setCurrentWidget(self.finishing_page)

    def on_finish_transaction(self):
        # Switch sidebar status view back to idle mode
        self.sidebar.set_status_state("idle")
        # Align page translation
        self.idle_page.update_language(self.sidebar.current_lang)
        # Show idle page
        self.stacked_widget.setCurrentWidget(self.idle_page)

    def load_fonts(self):
        font_dir = BASE_DIR / "resources"
        for font_file in ["MaterialSymbolsOutlined.ttf", "PlusJakartaSans.ttf", "SpaceGrotesk.ttf", "Inter.ttf"]:
            path = font_dir / font_file
            if path.exists():
                font_id = QFontDatabase.addApplicationFont(str(path))
                if font_id == -1:
                    print(f"[Warning] Failed to load font file: {font_file}")
            else:
                print(f"[Warning] Font file not found: {path}")
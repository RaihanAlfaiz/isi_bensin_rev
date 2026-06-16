from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
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

        # Connect signals
        self.sidebar.language_changed.connect(self.on_language_changed)
        self.idle_page.start_charging_clicked.connect(self.on_start_charging)
        self.plugin_page.proceed_to_payment.connect(self.on_proceed_to_payment)
        self.payment_page.payment_completed.connect(self.on_payment_completed)
        self.charging_page.charging_completed.connect(self.on_charging_completed)
        self.finishing_page.finish_clicked.connect(self.on_finish_transaction)

        # Add to layout with stretch factors for 20% / 80% proportion
        layout.addWidget(self.sidebar, 2)
        layout.addWidget(self.stacked_widget, 8)

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
        # Align page translation
        self.charging_page.update_language(self.sidebar.current_lang)
        # Show charging status page
        self.stacked_widget.setCurrentWidget(self.charging_page)

    def on_charging_completed(self):
        # Switch sidebar status view to finishing mode
        self.sidebar.set_status_state("finishing")
        # Pass variables to finishing page
        self.finishing_page.set_session_details(
            self.charging_page.seconds_elapsed,
            self.charging_page.energy_delivered
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
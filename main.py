import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen

def main():
    app = QApplication(sys.argv)

    main_window = None

    def on_splash_finished():
        nonlocal main_window
        main_window = MainWindow()
        main_window.show()

    # Create and show splash screen
    splash = SplashScreen(on_splash_finished)
    splash.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
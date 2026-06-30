import sys
import os
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test():
    from ui.main_window import MainWindow
    app = QApplication(sys.argv)
    
    try:
        w = MainWindow()
        w.show()
        print("MainWindow shown!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        
    # Quit after 3 seconds
    QTimer.singleShot(3000, app.quit)
    sys.exit(app.exec())

if __name__ == "__main__":
    test()

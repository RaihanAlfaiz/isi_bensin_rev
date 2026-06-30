import sys
import os
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt

def run_app_and_screenshot():
    from ui.main_window import MainWindow

    app = QApplication(sys.argv)
    
    # Enable exit on last window closed
    app.setQuitOnLastWindowClosed(True)

    main_window = MainWindow()
    main_window.show()
    print("MainWindow initialized and shown.")

    def grab_and_save(filename):
        os.makedirs("artifacts", exist_ok=True)
        pixmap = main_window.grab()
        pixmap.save(f"artifacts/{filename}")
        print(f"Saved artifacts/{filename}")

    def take_screenshot_idle():
        try:
            print("Taking idle screenshot...")
            grab_and_save("screenshot_idle.png")
            
            print("Triggering transition to PlugInState...")
            main_window.idle_page.start_charging_clicked.emit()
            
            # Wait 1.5 seconds for video buffering/rendering
            QTimer.singleShot(1500, take_screenshot_plugin)
        except Exception as e:
            import traceback
            traceback.print_exc()
            app.quit()
            
    def take_screenshot_plugin():
        try:
            print("Taking plugin screenshot...")
            grab_and_save("screenshot_plugin.png")
            
            print("Triggering transition to PaymentState...")
            main_window.plugin_page.proceed_to_payment.emit()
            
            QTimer.singleShot(1500, take_screenshot_payment)
        except Exception as e:
            import traceback
            traceback.print_exc()
            app.quit()

    def take_screenshot_payment():
        try:
            print("Taking payment screenshot...")
            grab_and_save("screenshot_payment.png")
            
            print("Triggering transition to ChargingState...")
            main_window.payment_page.payment_completed.emit()
            
            QTimer.singleShot(1500, take_screenshot_charging)
        except Exception as e:
            import traceback
            traceback.print_exc()
            app.quit()

    def take_screenshot_charging():
        try:
            print("Taking charging screenshot...")
            grab_and_save("screenshot_charging.png")
            
            print("Triggering transition to FinishingState...")
            main_window.charging_page.charging_completed.emit()
            
            QTimer.singleShot(1500, take_screenshot_finishing)
        except Exception as e:
            import traceback
            traceback.print_exc()
            app.quit()

    def take_screenshot_finishing():
        try:
            print("Taking finishing screenshot...")
            grab_and_save("screenshot_finishing.png")
            print("All screenshots taken successfully!")
        except Exception as e:
            import traceback
            traceback.print_exc()
        finally:
            app.quit()

    # Start the screenshot sequence after 1.5 seconds
    QTimer.singleShot(1500, take_screenshot_idle)

    sys.exit(app.exec())

if __name__ == "__main__":
    run_app_and_screenshot()

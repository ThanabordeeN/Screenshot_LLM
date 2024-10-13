import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from modules.screenshot_watcher import ScreenshotWatcher
from modules.ui import ScreenshotAnalyzer
from modules.tray_icon import SystemTrayApp

def main():
    app = QApplication(sys.argv)
    # Create the system tray icon
    tray_icon = QIcon("icon.ico")  # Ensure you have an icon.png in your project directory
    tray = SystemTrayApp(tray_icon)
    tray.setVisible(True)
    tray.show()

    watcher = ScreenshotWatcher()

    def on_screenshot_detected(image_path):
        window = ScreenshotAnalyzer(image_path)
        window.show()

    watcher.screenshot_detected.connect(on_screenshot_detected)
    watcher.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    main()
    root.withdraw()
    messagebox.showinfo("Info", "Programe ended")
    root.mainloop()
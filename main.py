import sys
from PyQt5.QtWidgets import QApplication
from modules.screenshot_watcher import ScreenshotWatcher
from modules.ui import ScreenshotAnalyzer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    watcher = ScreenshotWatcher()

    def on_screenshot_detected(image_path):
        window = ScreenshotAnalyzer(image_path)
        window.show()
    
    watcher.screenshot_detected.connect(on_screenshot_detected)
    watcher.start()

    sys.exit(app.exec_())
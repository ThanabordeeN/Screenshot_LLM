from PyQt5.QtCore import QThread, pyqtSignal
import os

class ScreenshotWatcher(QThread):
    screenshot_detected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        try:
            self.directory = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
            self.current_files = set(os.listdir(self.directory))
        except FileNotFoundError:
            self.directory = os.path.join(os.path.expanduser("~"), "OneDrive","Pictures", "Screenshots")
            self.current_files = set(os.listdir(self.directory))
            

    def run(self):
        while True:
            new_files = set(os.listdir(self.directory))
            if new_files != self.current_files:
                added_files = new_files - self.current_files
                if added_files:
                    recent_file = max(
                        added_files,
                        key=lambda f: os.path.getctime(os.path.join(self.directory, f)),
                    )
                    self.screenshot_detected.emit(os.path.join(self.directory, recent_file))
                self.current_files = new_files
            self.msleep(1000)  # Check every second
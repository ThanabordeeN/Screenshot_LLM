from PyQt6.QtCore import QThread, pyqtSignal
import os
import time

class ScreenshotWatcher(QThread):
    screenshot_detected = pyqtSignal(str)
    

    def __init__(self):
        super().__init__()
        self.directory = self.get_screenshot_directory()
        self.last_check_time = time.time()
        

    def get_screenshot_directory(self):
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")):
            return os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        else:
            return os.path.join(os.path.expanduser("~"), "OneDrive", "Pictures", "Screenshots")

    def run(self):
        while True:
            self.check_for_new_screenshots()
            self.msleep(1000)  # Check every second

    def check_for_new_screenshots(self):
        current_time = time.time()
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path) and os.path.getmtime(file_path) > self.last_check_time:
                self.screenshot_detected.emit(file_path)
        self.last_check_time = current_time
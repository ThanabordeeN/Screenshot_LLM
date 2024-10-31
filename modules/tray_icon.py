from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QAction
from .ui import ScreenshotAnalyzer

class SystemTrayApp(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayApp, self).__init__(icon, parent)
        self.create_menu()

    def create_menu(self):
        menu = QMenu()
        exit_action = QAction("Exit", self, triggered=self.exit_app)
        config_action = QAction("Config", self , triggered=self.config_app)
        menu.addAction(config_action)
        menu.addAction(exit_action)
        self.setContextMenu(menu)
        self.setToolTip("Screenshot LLM")

    def exit_app(self):
        QApplication.quit()
        
    def config_app(self):
        window = ScreenshotAnalyzer()
        window.show()

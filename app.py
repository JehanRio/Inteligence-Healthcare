import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.interface import Controller

# 配置日志级别和格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    controller.showHome()
    app.exec()
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_box = QLineEdit(self)
        self.button = QPushButton("点击我", self)
        self.button.clicked.connect(self.on_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_button_clicked(self):
        text = self.input_box.text()
        if text == "弹出弹窗":
            reply = QMessageBox.question(self, "确认", "你确定要弹出弹窗吗？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                print("用户点击了确认")
            else:
                print("用户点击了取消")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

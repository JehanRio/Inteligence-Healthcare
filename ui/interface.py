import os.path
import sys
import logging
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from ui import home, query, upload
from db.person import Person
from core.barCode import *
from db.mysqlConn import *

# 封装各个界面

class homeUi(QtWidgets.QMainWindow, home.Ui_Form):
    switchWindow2Query = QtCore.pyqtSignal()    # 跳转到query
    switchWindow2Upload = QtCore.pyqtSignal()    # 跳转到update

    def __init__(self):
        super(homeUi, self).__init__()
        self.setupUi(self)

        # 绑定
        self.queryButton.clicked.connect(self.goQuery)
        self.uploadButton.clicked.connect(self.goUpdate)

    def goQuery(self):
        self.switchWindow2Query.emit()
    def goUpdate(self):
        self.switchWindow2Upload.emit()

class queryUi(QtWidgets.QMainWindow, query.Ui_Form):
    switchWindow2Home = QtCore.pyqtSignal() # 返回主页面
    queryInfoByUploadImg = QtCore.pyqtSignal()  # 上传图片
    def __init__(self):
        super(queryUi, self).__init__()
        self.setupUi(self)

        # 绑定
        self.backButton.clicked.connect(self.goHome)
        self.uploadButton.clicked.connect(self.upload)

    def goHome(self):
        self.switchWindow2Home.emit()
    def upload(self):
        self.showInfo()
        logging.info("上传图片成功 展示病人信息")

    # 显示信息
    def showInfo(self):
        self.openImage()

    def openImage(self):  # 选择本地图片上传
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "result",
                                                       "*.png;;*.jpg;;All Files(*)")  # 弹出一个文件选择框，第一个返回值imgName记录选中的文件路径+文件名，第二个返回值imgType记录文件的类型

        jpg = QPixmap(imgName).scaled(self.code.width(),
                                            self.code.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长款
        self.code.setPixmap(jpg)  # 在label控件上显示选择的图片
        person = decode_barcode(imgName)

        self.name.setText(person.getName())
        self.gender.setText(person.getGender())
        self.age.setText(person.getAge())
        self.bloodType.setText(person.getBloodType())

        # 从数据库取数据
        medicine = queryindex2Medicine(person.getMedicine())
        self.medicine.setText(medicine)
        logging.info("病人信息：" + person.__str__())

class uploadUi(QtWidgets.QMainWindow, upload.Ui_Form):
    switchWindow2Home = QtCore.pyqtSignal() # 返回主页面
    uploadInfo = QtCore.pyqtSignal()    # 上传按钮
    def __init__(self):
        super(uploadUi, self).__init__()
        self.setupUi(self)

        # 绑定按钮的执行
        self.back.clicked.connect(self.goHome)
        self.uploadButton.clicked.connect(self.upload)

    def goHome(self):
        self.switchWindow2Home.emit()

    def upload(self):
        self.showInfo()

    # 病人信息
    def showInfo(self):
        name = self.name.text()
        gender = self.gender.text()
        age = self.age.text()
        bloodType = self.bloodType.text()
        medicine = self.medicine.text()
        codeType = self.codeType.currentText()

        # 封装成类
        person = Person(name, gender, age, bloodType, medicine)

        # 插入数据库
        # 先检查是否有姓名重复
        if checkRepetitive(name) == 0:
            reply = QMessageBox.question(self, "Warning!!!", "该病人已创建，是否覆盖信息？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:    # 覆盖信息 执行更新操作
                # 执行更新
                if queryMedicineandTransform(person) == -1:
                    reply = QMessageBox.question(self, "Warning!!!", "药品不存在", QMessageBox.Yes)
                    return
                updateByName(person)
                # 先删除文件
                codePath = os.path.join("result", name + "_" + codeType + ".png")
                try:
                    os.remove(codePath)
                    print(codePath)
                except FileNotFoundError:
                    print("文件不存在")
                # 生成条形码
                self.generateCode(person, codeType)
        else:
            if queryMedicineandTransform(person) == -1:
                reply = QMessageBox.question(self, "Warning!!!", "药品不存在", QMessageBox.Yes)
                return
            # 执行插入操作
            insert(person)
            self.generateCode(person, codeType)

    # 生成条形码
    def generateCode(self, person, codeType):
        # 生成条形码
        print(person.getMedicine())
        imgName = generate_barcode(person, codeType)
        jpg = QPixmap(imgName).scaled(self.code.width(),
                                      self.code.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长款

        self.code.setPixmap(jpg)  # 在label控件上显示选择的图片

        logging.info("病人信息：" + person.__str__() + "    " + "条形码生成：" + imgName)
        logging.info("上传病人信息成功 展示图片")

# 主要负责页面的切换，具体内部实现由具体的类实现
class Controller:
    def __init__(self):
        self.home = homeUi()
        self.upload = uploadUi()
        self.query = queryUi()

    def showHome(self):
        if self.upload.isVisible():
            self.upload.close()
        if self.query.isVisible():
            self.query.close()
        self.home = homeUi()
        self.home.show()

        # 绑定信号和槽（信号要执行的函数）
        self.home.switchWindow2Upload.connect(self.showUpload)
        self.home.switchWindow2Query.connect(self.showQuery)
    def showUpload(self):
        self.home.close()
        self.upload = uploadUi()
        self.upload.show()

        # 绑定信号和槽（信号要执行的函数）
        self.upload.switchWindow2Home.connect(self.showHome)
    def showQuery(self):
        self.home.close()
        self.query = queryUi()
        self.query.show()

        # 绑定信号和槽（信号要执行的函数）
        self.query.switchWindow2Home.connect(self.showHome)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    c = Controller()
    c.showHome()
    app.exec()
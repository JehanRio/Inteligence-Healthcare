# 用于后端之间传输 封装成类

class Person:
    def __init__(self, name:str, gender:str, age:str, bloodType:str, medicine:str):
        self.name = name
        self.gender = gender
        self.age = age
        self.bloodType = bloodType
        self.medicine = medicine

    def setName(self, name):
        self.name = name
    def setGender(self, gender):
        self.gender = gender
    def setAge(self, age):
        self.age = age
    def setBloodType(self, blood):
        self.bloodType = blood
    def setMedicine(self, medicine):
        self.medicine = medicine

    def getName(self):
        return self.name
    def getGender(self):
        return self.gender
    def getAge(self):
        return self.age
    def getBloodType(self):
        return self.bloodType
    def getMedicine(self):
        return self.medicine

    def __str__(self):
        return f"姓名：{self.name}, 性别：{self.gender}, 年龄：{self.age}, 血型：{self.bloodType}, 药物：{self.medicine}"

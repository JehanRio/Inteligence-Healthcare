# 用于对信息进行编码和解码

import barcode
import logging
import os
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image

from db.person import Person


def generate_barcode(person, encodeType):
    encodeData = person.getName() + " " + person.getGender() + " " + person.getAge() + " " + person.getBloodType() + " " + person.getMedicine()
    # 选择条形码类型
    codeType = barcode.get_barcode_class(encodeType)
    # 创建条形码对象
    try:
        barcode_obj = codeType(encodeData, writer=ImageWriter())
    except Exception as e:
        logging.error("输入数据格式有误，请检查！" + person)
        raise e
    # 保存条形码到文件
    output_file = os.path.join("result", person.name + "_" + encodeType)
    barcode_obj.save(output_file)
    return output_file

def decode_barcode(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    barcode_data = ''
    for obj in decoded_objects:
        barcode_data += obj.data.decode('utf-8')
    personList = barcode_data.split(" ")
    name = personList[0]
    gender = personList[1]
    age = personList[2]
    bloodType = personList[3]
    medicine = personList[4]
    person = Person(name, gender, age, bloodType, medicine)
    return person

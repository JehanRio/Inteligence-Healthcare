import barcode
from barcode.writer import ImageWriter

from pyzbar.pyzbar import decode
from PIL import Image

import logging

from db.person import Person


def generate_barcode(data, output_file):
    # 选择条形码类型，这里以Code128为例
    code128 = barcode.get_barcode_class('gs1_128')
    # 创建条形码对象
    barcode_obj = code128(data, writer=ImageWriter())
    # 保存条形码到文件
    barcode_obj.save(output_file)

def encode_demo():
    # 示例：将01字符串编码成条形码并保存为图片
    name = "lijiahan"
    gender = "male"
    age = str(22)
    blood = "A"
    medicine = "1,3,21"
    data = name + " " + gender + " " + age + " " + blood + " " + medicine
    output_file = 'barcode'
    generate_barcode(data, output_file)


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

def decode_demo():
    image_path = 'barcode.png'
    barcode_string = decode_barcode(image_path)
    print(barcode_string)



if __name__ == '__main__':
    encode_demo()
    decode_demo()
    # logging.info("错误！")
# 用于将数据存入mysql 并进行一些判断
import logging

import mysql.connector

from db.person import Person

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123456",
  database = "intelligenthealthcare"
)

def insert(person:Person):
  cursor = mydb.cursor()


  cursor.execute("INSERT INTO person (name, gender, age, blood_type, medicine) VALUES (%s, %s, %s, %s, %s)",
                 (person.name, person.gender, person.age, person.bloodType, person.medicine))
  mydb.commit()
  cursor.close()

def updateByName(person:Person):
  cursor = mydb.cursor()
  name = person.getName()
  cursor.execute("update person set gender = %s, age = %s, blood_type = %s, medicine = %s where name = %s",
                 (person.getGender(), person.getAge(), person.getBloodType(), person.getMedicine(), name))
  # cursor.execute("update person set gender = 'female' where name = 'jehan'")
  mydb.commit()
  cursor.close()
  print("over")

def checkRepetitive(name:str):
  cursor = mydb.cursor()
  query = "SELECT EXISTS(SELECT 1 FROM person WHERE name = %s)"
  cursor.execute(query, (name,))
  result = cursor.fetchone()[0]
  # 用户重复 抛出异常
  if result == 1:
    return 0
  cursor.close()
  return 1

# 将药品转换成数据库索引
def queryMedicineandTransform(person:Person):
  with mydb.cursor() as cursor:
    name = person.getName()
    medicine = person.getMedicine()
    # cursor.execute("select id from person where name = %s", (name,))
    # personId = cursor.fetchone()[0]
    medicine_list = medicine.split(',')
    res = []
    for m in medicine_list:
      query = "select id from medicine where drug_name = %s"
      cursor.execute(query, (m,))
      result = cursor.fetchone()
      if result:
        medicine_Id = result[0]
        res.append(str(medicine_Id))
        # cursor.execute("insert into person_medicine (person_id, medicine_id) values (%s, %s)", (personId, medicine_Id,))
      else:
        return -1
    person.setMedicine(','.join(res))
  return 1

def queryindex2Medicine(medicine:str):
  res = []
  with mydb.cursor() as cursor:
    list = medicine.split(',')
    for i in list:
      query = "select drug_name from medicine where %s = id"
      cursor.execute(query, (i, ))
      res.append(cursor.fetchone()[0])
  # print(','.join(res))
  return ','.join(res)
if __name__ == '__main__':
  # queryMedicineandTransform("阿司匹林,布洛芬,999感冒灵颗粒")
  queryindex2Medicine("1,2,13")
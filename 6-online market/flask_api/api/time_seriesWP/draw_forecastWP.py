# مكتبة الاتصال مع قاعدة البيانات
import mysql.connector
# مكتبة بانداس
import pandas as pd
import os

# تعريف دالة للاتصال بقاعدة البيانات
connection_mydb = None
cursor = None
def mysql_connect():
    # الاتصال مع قاعدة البيانات
    global cursor, connection_mydb
    connection_mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="market"
    )
    # مؤشر
    cursor = connection_mydb.cursor(dictionary=True)

def create_img():
  # الاتصال مع قاعدة البيانات
  mysql_connect()

  # مكتبة الرسم
  import matplotlib.pyplot as plt
  # قياس الرسم
  plt.figure(figsize=(12,10))
  # الستعلام عن بيانات جدول التوقع المخصص
  sql='''SELECT * from custom_forecast'''
  # التنفيذ وتمرير قيمة المعامل
  cursor.execute(sql)
  # جلب كل النتائج
  results = cursor.fetchall()
  #إطار بيانات للنتائج
  df=pd.DataFrame(columns=['date','total'])
  # الدوران على النتائج
  for row in results:
      obj={
              "date":row['date'],
              "total":row['total']}
      # الإضافة إلى إطار البيانات
      # df=df.append(obj, ignore_index=True)
      df = pd.concat([df, pd.DataFrame([obj])], ignore_index=True)

  # رسم خط
  # المحور الأفقي هو التاريخ
  # المحور العمودي هو المبيعات
  plt.plot(df['date'],df['total'])
  # تسمية المحور الأفقي
  plt.xlabel("Date")
  # تسمية المحور العمودي
  plt.ylabel("Expected Total")
  # عنوان الرسم
  plt.title("Sales Forecast")
  # الإظهار
  # plt.show()
  connection_mydb.close()
  # حفظ المخطط بشكل صورة png
  path = "output_img.png"
  plt.savefig(path, format='png')
  import base64
  # فتح الملف وتحويل الصورة الى base64
  with open(path, 'rb') as image_file:
    image_data = image_file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
  # ارجاع رد عبارة عن src للصورة
  return f"data:image/jpeg;base64,{base64_image}"
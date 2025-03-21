import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DSN = os.getenv('DB_DSN')

conn = oracledb.connect(
    user = DB_USER,
    password = DB_PASSWORD,
    dsn = DB_DSN
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM SYSTEM.CUSTOMER")

row = cursor.fetchall()

if row:
    for i in row:
        print(i)
else:
    print("tabla no encontrada" , row)
    
cursor.close()
conn.close()
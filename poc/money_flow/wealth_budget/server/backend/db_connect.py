import os
import mysql.connector

DBconn = mysql.connector.connect(
    user = "mainuser",
    password = os.environ.get('WBDBPASS'),
    host = 'localhost',
    port = 13307,
    database = 'wb_users'
)
DBw = DBconn.cursor(dictionary=True)
print('CONNECTED. WRITER:', DBw)

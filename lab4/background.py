#!/usr/bin/env python3

import mysql.connector
import time

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    database = "abhi",
    autocommit = True)
	
mycursor  = mydb.cursor()

i=1
while True:
	time.sleep(300)
	mycursor.execute("delete from Session")
	print(i," Session table has been cleared")
	i = i+1


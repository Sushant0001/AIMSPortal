import mysql.connector
import pandas as pd
import hashlib

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    database = "abhi",
    autocommit = True)
	
mycursor  = mydb.cursor()


'''
	
data = pd.read_csv("student.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Student(ID varchar(20),Name varchar(100),DOB varchar(100),Contact varchar(100),Branch varchar(10),Email varchar(100));")
for row in df.itertuples():
	stmt = "insert into Student values('"+str(row.ID)+"','"+row.Name+"','"+row.DOB+"','"+str(row.Contact)+"','"+row.Branch+"','"+row.Email+"')"
	print(stmt)
	mycursor.execute(stmt)


data = pd.read_csv("prof.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Professor(ID varchar(20),Name varchar(100),Email varchar(100));")
for row in df.itertuples():
	stmt = "insert into Professor values('"+str(row.ID)+"','"+row.Name+"','"+row.Email_id+"')"
	print(stmt)
	mycursor.execute(stmt)


data = pd.read_csv("courses.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Courses(ID varchar(20),Name varchar(100),L varchar(3),T varchar(3),P varchar(3),S varchar(3),C varchar(3));")
for row in df.itertuples():
	stmt = "insert into Courses values('"+str(row.ID)+"','"+str(row.Name)+"','"+str(row.L)+"','"+str(row.T)+"','"+str(row.P)+"','"+str(row.S)+"','"+str(row.C)+"')"
	print(row)
	mycursor.execute(stmt)



data = pd.read_csv("staff.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Staff(ID varchar(20),Name varchar(100),Email varchar(100));")
for row in df.itertuples():
	stmt = "insert into Staff values('"+str(row.ID)+"','"+row.Name+"','"+row.Email_id+"')"
	mycursor.execute(stmt)
	print(stmt)
	
	


data = pd.read_csv("user.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table User(Type varchar(2),ID varchar(20),Name varchar(100),Password varchar(500));")
for row in df.itertuples():
	password = hashlib.sha256(row.Password.encode())
	stmt = "insert into User values('"+str(row.Type)+"','"+str(row.ID)+"','"+row.Username+"','"+str(password.hexdigest())+"')"
	print(stmt)
	mycursor.execute(stmt)
	


data = pd.read_csv("prereq.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Prereq(ID varchar(20),Prereq varchar(20));")
for row in df.itertuples():
	stmt = "insert into Prereq values('"+str(row.ID)+"','"+row.Course_Pre_Req+"')"
	mycursor.execute(stmt)
	print(stmt)


data = pd.read_csv("Completed.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Completed(Course_ID varchar(20),Student_ID varchar(20),Points varchar(4),Semester varchar(4));")
for row in df.itertuples():
	stmt = "insert into Completed values('"+row.Course_ID+"','"+row.Student_ID+"','"+str(row.Points)+"','"+str(row.Semester)+"')"
	mycursor.execute(stmt)
	print(stmt)

	

data = pd.read_csv("Current.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Current(Course_ID varchar(20),Student_ID varchar(20),Semester varchar(4));")
for row in df.itertuples():
	stmt = "insert into Current values('"+row.Course_ID+"','"+row.Student_ID+"','"+str(row.Semester)+"')"
	mycursor.execute(stmt)
	print(stmt)	
	

data = pd.read_csv("Offered.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Offered(Course_ID varchar(20),Faculty_ID varchar(20),Required_CGPA varchar(4));")
for row in df.itertuples():
	stmt = "insert into Offered values('"+row.Course_ID+"','"+row.Faculty_ID+"','"+str(row.Required_CGPA)+"')"
	mycursor.execute(stmt)
	print(stmt)	


data = pd.read_csv("Semester.csv")
df = pd.DataFrame(data)
print(df)
#mycursor.execute("create table Semester(Year varchar(20),Sem varchar(4));")
for row in df.itertuples():
	stmt = "insert into Semester values('"+str(row.Year)+"','"+str(row.Sem)+"')"
	mycursor.execute(stmt)
	print(stmt)


mycursor.execute("create table Session(User_ID varchar(20),Time varchar(20))")



data = pd.read_csv("Info.csv")
df = pd.DataFrame(data)
print(df)
mycursor.execute("create table Info(ID varchar(20),Contact varchar(20));")
for row in df.itertuples():
	stmt = "insert into Info values('"+str(row.ID)+"','"+str(row.Contact)+"')"
	mycursor.execute(stmt)
	print(stmt)
	
'''

import mysql.connector
import time
import os
import pandas as pd

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    database = "abhi",
    autocommit = True)
	
mycursor  = mydb.cursor()


def view_registered_student_list():
    course_id = input("Enter course ID : ").upper()
    mycursor.execute("select * from Current where Course_ID = %s",(course_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("No students registered for this course !!")
        time.sleep(8)
        return

    print("     Enrolled Students in ",course_id,)
    for i in range(len(result)):
        mycursor.execute("select * from Student where ID = %s",(result[i][1],))
        result2 = mycursor.fetchall()
        print(result2[0][0],result2[0][1])
    time.sleep(8)

def view_grade():
    course_id = input("Enter course ID : ").upper()
    mycursor.execute("select * from Semester")
    result = mycursor.fetchall()
    cur_year = int(result[0][0])
    cur_sem = int(result[0][1])

    mycursor.execute("select * from Completed where Course_ID = %s",(course_id,))
    result = mycursor.fetchall()
    count = 0
    print("     Student's Grade")
    for i in range(len(result)):
        student_id = result[i][1]
        completed_sem = result[i][3]
        completed_sem = int(completed_sem)
        admission_year = student_id[:4]
        admission_year = int(admission_year)
        value = (cur_year - admission_year)*2 + cur_sem
        if (value - completed_sem) == 0:
            mycursor.execute("select * from Student where ID = %s",(student_id,))
            result2 = mycursor.fetchall()
            print(result2[0][0],result2[0][1],result[i][2])
            count = count + 1
    
    if count == 0:
        print("Students didn't received any grade !!")

    time.sleep(8)


def offer_course(faculty_id):
    course_id = input("Enter course ID : ").upper()
    mycursor.execute("select * from Courses where ID = %s",(course_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("This course is not available to offer !!")
        time.sleep(8)
        return
    mycursor.execute("select * from Offered where Course_ID = %s",(course_id,))
    result = mycursor.fetchall()
    if(len(result) != 0):
        print("This course is already offered !!")
        time.sleep(8)
        return
    required_cgpa = input("Enter required CGPA to enroll to this course : ")
    mycursor.execute("insert into Offered values(%s,%s,%s)",(course_id,faculty_id,required_cgpa,))
    print("Course has been offered by You !!")
    time.sleep(8)

def upload_grade(faculty_id):
    course_id = input("Enter course ID which you want to Grade : ").upper()
    mycursor.execute("select * from Offered where Course_ID = %s and Faculty_ID = %s",(course_id,faculty_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("This course is not Offere by you !!")
        time.sleep(8)
        return
    filename = input("Enter File name of grades : ")
    path="/home/sushant/PGLAB/lab4/"+filename
    isFile = os.path.isfile(path)
    if isFile:        
        data = pd.read_csv(filename)
        df = pd.DataFrame(data)
        print(df)
        for row in df.itertuples():
            mycursor.execute("select * from Current where Student_ID = %s and Course_ID = %s",(row.Student_ID,course_id,))
            result = mycursor.fetchall()
            if(len(result) == 0):
                print(row.Student_ID,"is not enrolled for this course ! ")
            else:
                mycursor.execute("delete from Current where Course_ID = %s and Student_ID = %s",(course_id,row.Student_ID,))
                mycursor.execute("insert into Completed values(%s,%s,%s,%s)",(course_id,row.Student_ID,str(row.Grade),result[0][2]))
        print("Grades has been updated !!")
        time.sleep(8)
    else:
        print("NO "+filename+" file exists !!!")
        time.sleep(8)

def view_offered_courses():
    mycursor.execute("select * from Offered")
    result = mycursor.fetchall()
    print("Course_ID Course_Name Faculty_ID Required_CGPA")
    for i in range(len(result)):
        mycursor.execute("select * from Courses where ID = %s",(result[i][0],))
        result2 = mycursor.fetchall()
        print(result[i][0],result2[0][1],result[i][1],result[i][2])
    time.sleep(8)

def view_transcript():
    student_id = input("Enter student id : ").upper()
    mycursor.execute("select * from Student where ID = %s",(student_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("No such student exist in Database ")
        time.sleep(5)
    else:
        student_name = result[0][1]
        print("     Name : ",student_name," Roll NO. : ",student_id)
        mycursor.execute("select * from Completed where Student_ID = %s order by Semester",(student_id,))
        result = mycursor.fetchall()
        sem = 0
        cgpa = 0
        sgpa = 0
        counter = 0
        cgpacounter = 0


        for i in range(len(result)):
            if sem != result[i][3]:
                sem = result[i][3]
                if(sgpa != 0 and counter != 0):
                    print("     SGPA : ",sgpa/counter)
                    counter = 0
                    sgpa = 0
                print("     Semester : ",sem)
            mycursor.execute("select Name from Courses where ID = %s",(result[i][0],))
            result2 = mycursor.fetchall()
            subject_name = result2[0][0]
           
            if(result[i][2] != "-1"):
                cgpa = cgpa + float(result[i][2])
                sgpa = sgpa + float(result[i][2])
                counter = counter + 1
            
            if(result[i][2] != "-1"):
                print("     ",result[i][0],subject_name,result[i][2])
                cgpacounter = cgpacounter + 1
            else:
                print("     ",result[i][0],subject_name,"W")



        if(counter!=0):
            print("     SGPA : ",sgpa/counter)
        else:
            print("     SGPA : ",sgpa)
        if(cgpacounter!=0):
            print("     CGPA : ",cgpa/cgpacounter)
        else:
            print("     CGPA : ",cgpa)
        time.sleep(100)



def update_contact(user_id):
    mob = input("Enter your mobile number : ")
    mycursor.execute("update Info set Contact = %s where ID = %s",(mob,user_id,))
    print("Contact is successfully updated !!")
    time.sleep(5)

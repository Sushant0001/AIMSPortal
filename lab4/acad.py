import mysql.connector
import time
import os
mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    database = "abhi",
    autocommit = True)
	
mycursor  = mydb.cursor()



def create_course():
    print("Enter course ID : ")
    course_id = input()
    mycursor.execute("select * from Courses where ID = %s",(course_id,))
    result = mycursor.fetchall()
    if(len(result)!=0):
        print("Course already exists !!")
        time.sleep(8)
        return
    course_id = course_id.upper()
    print("Enter course name : ")
    course_name = input()
    print("Enter L T P S C")
    l = input()
    t = input()
    p = input()
    s = input()
    c = input()
    print("How many pre requisite are there : ")
    n = int(input())
    if(n>2):
        print("Pre requisites count is too high ")
        time.sleep(3)
        return
    if(n>0):
        pre_req_list = []
        for i in range(n):
            print("Enter pre requisite ID :" )
            pre_id = input().upper()
            mycursor.execute("select * from Courses where ID = %s",(pre_id,))
            result = mycursor.fetchall()
            if len(result) == 0:
                print("No such course exists.")
                time.sleep(3)
                return
            else:
                pre_req_list.append(pre_id) 
        
        for i in range(n):
            pre_id = pre_req_list[i]
            mycursor.execute("insert into Prereq values(%s,%s)",(course_id,pre_id,))
        sql = "insert into Courses values(%s,%s,%s,%s,%s,%s,%s)"
        values = (course_id,course_name,l,t,p,s,c)
        mycursor.execute(sql,values)
        print("Course successfully created")
        time.sleep(3)

    if(n == 0):
        sql = "insert into Courses values(%s,%s,%s,%s,%s,%s,%s)"
        values = (course_id,course_name,l,t,p,s,c)
        mycursor.execute(sql,values)        
        print("Course successfully created")
        time.sleep(3)
    

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
                    if(counter!=0):
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
        if(cgpacounter != 0):
            print("     CGPA : ",cgpa/cgpacounter)
        else:
            print("     CGPA : ",cgpa)
        time.sleep(5)

def generate_transcript():
    student_id = input("Enter student id : ").upper()
    mycursor.execute("select * from Student where ID = %s",(student_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("No such student exist in Database ")
        time.sleep(5)
    else:
        f = open(student_id+".txt","w")
        student_name = result[0][1]
        f.write("     Name : "+student_name+" Roll NO. : "+student_id+"\n")
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
                    f.write("     SGPA : "+str(sgpa/counter)+"\n")
                    counter = 0
                    sgpa = 0
                f.write("     Semester : "+sem+"\n")
            mycursor.execute("select Name from Courses where ID = %s",(result[i][0],))
            result2 = mycursor.fetchall()
            subject_name = result2[0][0]
            if(result[i][2] != "-1"):
                cgpa = cgpa + float(result[i][2])
                sgpa = sgpa + float(result[i][2])
                counter = counter + 1
            
            if(result[i][2] != "-1"):
                f.write("     "+result[i][0]+" "+subject_name+" "+result[i][2]+"\n")
                cgpacounter = cgpacounter + 1
            else:
                f.write("     "+result[i][0]+" "+subject_name+" W"+"\n")
        if(counter!=0):
            f.write("     SGPA : "+str(sgpa/counter)+"\n")
        else:
            f.write("     SGPA : "+str(sgpa)+"\n")
        if(cgpacounter!=0):
            f.write("     CGPA : "+str(cgpa/cgpacounter)+"\n")
        else:
            f.write("     CGPA : "+str(cgpa)+"\n")
        
        print("Transcript has been generated Successfully !!")
        print("File name : ",os.path.basename(student_id+".txt"))
        print("Directory name : ",os.path.dirname(__file__))
        f.close()
        time.sleep(8)

def update_contact(user_id):
    mob = input("Enter your mobile number : ")
    mycursor.execute("update Info set Contact = %s where ID = %s",(mob,user_id,))
    print("Contact is successfully updated !!")
    time.sleep(5)
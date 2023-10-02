from unittest import result
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

def register_to_course(student_id):
    mycursor.execute("select * from Current where Student_ID = %s",(student_id,))
    result = mycursor.fetchall()
    total_credits_enrolled = 0
    for i in range(len(result)):
        mycursor.execute("select * from Courses where ID = %s",(result[i][0],))
        result2 = mycursor.fetchall()
        total_credits_enrolled = total_credits_enrolled + int(result2[0][6])
        print(result[i][0],result2[0][6])
    print("Total credits you have enrolled are : ",total_credits_enrolled)

    mycursor.execute("select * from Completed where Student_ID = %s order by Semester",(student_id,))
    result = mycursor.fetchall()
    count =  0
    credits_done = 0
    sem = 0
    for i in range(len(result)):
        if(float(result[i][2]) >= 4):
            print(result[i])
            sem = int(result[i][3])
            count = count + 1
            mycursor.execute("select * from Courses where ID = %s",(result[i][0],))
            result2 = mycursor.fetchall()
            credits_done = credits_done + float(result2[0][6])
    print("Total credits done are : ",credits_done)
    credits_can_enroll = 30
    if sem!=0:
        credits_can_enroll = 1.25*credits_done/sem - total_credits_enrolled
    print("Total credits you can enroll are : ",credits_can_enroll)
    mycursor.execute("select * from Offered")
    result = mycursor.fetchall()
    print("     Offered courses are : ")
    for i in result:
        print(i)
    enrolling_course = input("which course you want to enroll (Enter course ID) : ").upper()
    course_available = False
    for i in range(len(result)):
        if(enrolling_course == result[i][0]):
            course_available = True
            break

    if course_available:
        check_p = check_prereq(student_id,enrolling_course)
        if check_p:
            mycursor.execute("select * from Current where Course_ID = %s and Student_ID = %s",(enrolling_course,student_id,))
            result2 = mycursor.fetchall()
            if(len(result2) != 0):
                print("You are already enrolled to this course ")
            else:
                if sem == 0:
                    mycursor.execute("insert into Current values(%s,%s,%s)",(enrolling_course,student_id,str(sem+1),))
                    print("You have been registered to course ",enrolling_course," !!")
                else:
                    student_cgpa = calculate_cgpa(student_id)
                    mycursor.execute("select * from Offered where Course_ID = %s",(enrolling_course,))
                    result = mycursor.fetchall()
                    if(student_cgpa <= float(result[0][2])):
                        print("Your required CGPA is less to register for this course ")
                    else:
                        mycursor.execute("select * from Courses where ID = %s",(enrolling_course,))
                        result2 = mycursor.fetchall()
                        if credits_can_enroll - float(result2[0][6]) >= 0:
                            mycursor.execute("insert into Current values(%s,%s,%s)",(enrolling_course,student_id,str(sem+1),))
                            print("You have been registered to course ",enrolling_course," !!")
                        else:
                            print("You can't enroll to this course (Credit limit reached !)")
        else:
            print("You have not completed pre requisites for this Course ")            
    else:
        print("This course is not available to enroll ")
    time.sleep(10)
    
def calculate_cgpa(student_id):
    mycursor.execute("select * from Completed where Student_ID = %s order by Semester",(student_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("NO CGPA available ")
        return 0
    sem = 0
    cgpa = 0
    sgpa = 0
    counter = 0
    cgpacounter = 0
    for i in range(len(result)):
        if sem != result[i][3]:
            sem = result[i][3]
            if(sgpa != 0 and counter != 0):
                #print("     SGPA : ",sgpa/counter)
                counter = 0
                sgpa = 0
            #print("     Semester : ",sem)
        mycursor.execute("select Name from Courses where ID = %s",(result[i][0],))
        result2 = mycursor.fetchall()
        subject_name = result2[0][0]
        if(result[i][2] != "-1"):
            cgpa = cgpa + float(result[i][2])
            sgpa = sgpa + float(result[i][2])
            counter = counter + 1
        
        if(result[i][2] != "-1"):
            #print("     ",result[i][0],subject_name,result[i][2])
            cgpacounter = cgpacounter + 1
        #else:
            #print("     ",result[i][0],subject_name,"W")
    #if(counter!=0):
        #print("     SGPA : ",sgpa/counter)
    #else:
        #print("     SGPA : ",sgpa)
    print("     CGPA : ",cgpa/cgpacounter)
    #time.sleep(5)
    return cgpa/cgpacounter


def check_prereq(student_id,enrolling_course):
    mycursor.execute("select * from Prereq where ID = %s",(enrolling_course,))
    result = mycursor.fetchall()
    req = 0
    for i in range(len(result)):
        mycursor.execute("select * from Completed where Course_ID = %s and Student_ID = %s and Points != %s and Points != %s",(result[i][1],student_id,"0","-1"))
        result2 = mycursor.fetchall()
        if(len(result2) != 0):
            req = req + 1
    if(req == len(result)):
        return True
    else:
        return False



def deregister_course(student_id):
    mycursor.execute("select Course_ID from Current where Student_ID = %s",(student_id,))
    result = mycursor.fetchall()
    print("Your enrolled Courses are : ")
    for i in result:
        print(i)
    course_id = input("Enter course id you want to deregister ")
    mycursor.execute("select * from Current where Course_ID = %s and Student_ID = %s",(course_id,student_id,))
    result = mycursor.fetchall()
    if(len(result)==0):
        print("You are not enrolled to this course ! ")
    else:
        mycursor.execute("delete from Current where Course_ID = %s and Student_ID = %s",(course_id,student_id,))
        mycursor.execute("insert into Completed values(%s,%s,%s,%s)",(result[0][0],result[0][1],"-1",result[0][2]))
        print("You have been Successfully withdrawn your course",course_id)
    time.sleep(8)

def compute_cgpa(student_id):
    mycursor.execute("select * from Completed where Student_ID = %s order by Semester",(student_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("NO CGPA available ")
        return
    sem = 0
    cgpa = 0
    sgpa = 0
    counter = 0
    cgpacounter = 0
    for i in range(len(result)):
        if sem != result[i][3]:
            sem = result[i][3]
            if(sgpa != 0 and counter != 0):
                #print("     SGPA : ",sgpa/counter)
                counter = 0
                sgpa = 0
            #print("     Semester : ",sem)
        mycursor.execute("select Name from Courses where ID = %s",(result[i][0],))
        result2 = mycursor.fetchall()
        subject_name = result2[0][0]
        if(result[i][2] != "-1"):
            cgpa = cgpa + float(result[i][2])
            sgpa = sgpa + float(result[i][2])
            counter = counter + 1
        
        if(result[i][2] != "-1"):
            #print("     ",result[i][0],subject_name,result[i][2])
            cgpacounter = cgpacounter + 1
        #else:
            #print("     ",result[i][0],subject_name,"W")
    #if(counter!=0):
        #print("     SGPA : ",sgpa/counter)
    #else:
        #print("     SGPA : ",sgpa)
    if(cgpacounter!=0):
        print("     Your current CGPA is : ",cgpa/cgpacounter)
    else:
        print("     Your current CGPA is : ",cgpa)
    time.sleep(8)
    #return cgpa/cgpacounter


def view_gradesheet(student_id):
    mycursor.execute("select * from Student where ID = %s",(student_id,))
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("No such student exist in Database ")
    else:
        student_name = result[0][1]
        print("     Name : ",student_name," Roll NO. : ",student_id)
        mycursor.execute("select * from Completed where Student_ID = %s order by Semester",(student_id,))
        result = mycursor.fetchall()
        if(len(result) == 0):
            print("NO CGPA available ")
            return  
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
        if(cgpacounter != 0):
            print("     CGPA : ",cgpa/cgpacounter)
        else:
            print("     CGPA : ",cgpa)
        time.sleep(8)

def update_contact(user_id):
    mob = input("Enter your mobile number : ")
    mycursor.execute("update Info set Contact = %s where ID = %s",(mob,user_id,))
    print("Contact is successfully updated !!")
    time.sleep(5)
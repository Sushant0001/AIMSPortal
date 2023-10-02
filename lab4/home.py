import mysql.connector
import os
from getpass import getpass
import hashlib
import os
import time
import datetime
import acad
import fac
import stud

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    database = "abhi",
    autocommit = True)
	
mycursor  = mydb.cursor()



def welcome_screen():
    os.system("clear")
    mycursor.execute("select * from Semester")
    data = mycursor.fetchall()
    print("Year : ",data[0][0],"Semester : ",data[0][1])

    print("""Welcome to AIMS portal 

Please login to continue

1: Student 
2: Faculty 
3: Academics
4:EXIT
""")

    user_type = input()
    if user_type == "4":
        exit()
    # user_type = 3
    # username = "admin"
    # password = "password"

    if user_type not in ["1","2","3"]:
        print("No such user type. Please try again")
        time.sleep(3)
        welcome_screen()

    username = input("Username: ")
    password = getpass()
    success,user_id = login(user_type,username,password)
    
    if success:
        if user_type == "3":
            print("going to acadmics",user_id)
            academics(user_id)
        elif user_type == "2":        
            print("going to faculty",user_id)
            faculty(user_id)
        elif user_type == "1":
            print("going to Student",user_id)
            student(user_id)
    else:
        print("Login denied. Please try again")
        time.sleep(3)
        welcome_screen()


def login(user_type,username,password):
    

    sql = "SELECT * FROM User WHERE Type = %s AND Name = %s"
    val = (user_type,username)
    mycursor.execute(sql,val)
    results = mycursor.fetchall()

    if len(results) == 0:
        print("No such user present in database")
        return False,None

    if len(results) == 1:
        passw = hashlib.sha256(password.encode())
        passw = str(passw.hexdigest())
        #print("hashed pass is : ",hashed_pass)
        if results[0][3] == passw:
            
            mycursor.execute("select * from Session where User_ID = %s",(results[0][1],))
            info = mycursor.fetchall()
            if(len(info) != 0):
                print("You are already logged in !!")

                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                sql = "insert into Session values(%s,%s)"
                val = (results[0][1],timestamp)

                mycursor.execute(sql,val)
                time.sleep(2)
                return True,results[0][1]
            else:
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                sql = "insert into Session values(%s,%s)"
                val = (results[0][1],timestamp)

                mycursor.execute(sql,val)
                
                print("Login successful")
                time.sleep(1)

                return True,results[0][1]
        else:
            print("Login Denied: Wrong password")
            return False,None
    else:
        print("Multiple users present. Contact Admin")
        return False,None





def academics(user_id):
    """
    Function that displays home screen for academic users
"""
    os.system("clear")
    print(""" Welcome Academics office user

1. Logout.
2. Create course.
3. View transcript of a student.
4. Generate transcript for a student(.txt).
5. Update your contact
""")

    option = input()

    if option == "1":
        logout(user_id)
        welcome_screen()
    if option == "2":
        if(user_id != "IIT1006"):
            print("You are not allowed to this operation !! ")
            time.sleep(4)
        else:
            acad.create_course()
        academics(user_id)
    if option == "3":
        acad.view_transcript()
        academics(user_id)
    if option == "4":
        acad.generate_transcript()
        academics(user_id)
    if option == "5":
        acad.update_contact(user_id)
        academics(user_id)
    else:
        print("Please enter correct option !!")
        time.sleep(3)
        academics(user_id)



def student(user_id):
    """
Function that displays home screen for student users
"""
    os.system("clear")
    print(""" Welcome student

1. Logout.
2. Register to course.
3. Deregister(Withdraw) to course.
4. Compute current CGPA.
5. View my gradesheet.
6. Update your contact
    """)

    option = input()
    
    if option == "1":
        logout(user_id)
        welcome_screen()
    if option == "2":
        stud.register_to_course(user_id)
        student(user_id)
    if option == "3":
        stud.deregister_course(user_id)
        student(user_id)
    if option == "4":
        stud.compute_cgpa(user_id)
        student(user_id)
    if option == "5":
        stud.view_gradesheet(user_id)
        student(user_id)
    if option == "6":
        stud.update_contact(user_id)
        student(user_id)
    else:
        raise NotImplementedError()



def faculty(user_id):
    """
    Function that displays home screen for faculty users
    """
    os.system("clear")
    print(""" Welcome Faculty office user

    1. Logout.
    2. View student list registered for a course. 
    3. View grade of all students registered to course in current semester.
    4. Offer a course.
    5. Upload grade via .CSV file.
    6. View all offered courses in current semester.
    7. View grades of student for all subjects. 
    8. Update your contact
    """)

    option = input()

    if option == "1":
        logout(user_id)
        welcome_screen()
    if option == "2":
        fac.view_registered_student_list()
        faculty(user_id)
    if option == "3":
        fac.view_grade()
        faculty(user_id)
    if option == "4":
        fac.offer_course(user_id)
        faculty(user_id)
    if option == "5":
        fac.upload_grade(user_id)
        faculty(user_id)
    if option == "6":
        fac.view_offered_courses()
        faculty(user_id)
    if option == "7":
        fac.view_transcript()
        faculty(user_id)
    if option == "8":
        fac.update_contact(user_id)
        faculty(user_id)
    else:
        print("Please enter correct option !!")
        faculty(user_id)



def logout(user_id):
    sql = "DELETE FROM Session WHERE User_ID =  %s"
    val = (user_id,)

    mycursor.execute(sql,val)
    print("logged out")
    time.sleep(1)

os.system("nohup python3 -u /home/sushant/PGLAB/lab4/background.py output.log &")
os.system("clear")
welcome_screen()

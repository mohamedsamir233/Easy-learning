from PyQt5 import QtCore , Qt , uic , QtCore , uic
from PyQt5.QtWidgets import QMessageBox , QMainWindow , QLineEdit , QApplication
from PyQt5.QtCore import  *
from PyQt5.QtGui import * 
import sys
from PyQt5 import QtTest
import mysql.connector
import re
w = 550
h = 501

db = mysql.connector.connect (
    host = "localhost" ,
    user = "root" ,
    password = "12345678" ,
    database = "easydb"
)

mycursor = db.cursor ()

class main(QMainWindow):

    def __init__(self):
        super(main, self).__init__()
        uic.loadUi("first.ui", self)
        self.UI()
        self.Buttons()
        self.show()
        self.tabWidget.tabBar().setVisible(False)

    def UI (self) :
        self.setWindowTitle ("Easy Learning ")
        self.resize(w,h)
        self.setWindowIcon(QIcon("bin/icon.ico"))
        self.lineEdit.setAlignment(Qt.AlignJustify)
        self.lineEdit_2.setAlignment(Qt.AlignJustify)
        self.lineEdit_3.setAlignment(Qt.AlignJustify)
        self.lineEdit_4.setAlignment(Qt.AlignJustify)
        self.lineEdit_5.setAlignment(Qt.AlignJustify)
        self.lineEdit_6.setAlignment(Qt.AlignJustify)
        self.lineEdit_7.setAlignment(Qt.AlignJustify)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def Buttons (self) :
        self.pushButton_2.clicked.connect (self.show_pass)
        self.pushButton_4.clicked.connect (self.forgetScreen)
        self.pushButton_3.clicked.connect (self.registerScreen)
        self.pushButton_6.clicked.connect (self.exit)
        self.pushButton_7.clicked.connect (self.maximize)
        self.pushButton_8.clicked.connect (self.Minimize)
        self.pushButton_11.clicked.connect (self.show_pass)
        self.pushButton_10.clicked.connect (self.create_Acc)
        self.pushButton.clicked.connect (self.login)
    
    def password_check(self,passwd):

        SpecialSym =['$', '@', '#', '%']
        val = True
        if len(passwd) < 6:
            print('length should be at least 6')
            val = False
            QMessageBox.critical (self,"Register " , "length should be at least 6" )

        if len(passwd) > 20:
            print('length should be not be greater than 8')
            val = False
            QMessageBox.critical (self,"Register " , "length should be not be greater than 8" )

        if not any(char.isdigit() for char in passwd):
            print('Password should have at least one numeral')
            val = False
            QMessageBox.critical (self,"Register " , "Password should have at least one numeral" )
            

        if not any(char.isupper() for char in passwd):
            print('Password should have at least one uppercase letter')
            val = False
            QMessageBox.critical (self,"Register " , "Password should have at least one uppercase letter" )

        if not any(char.islower() for char in passwd):
            print('Password should have at least one lowercase letter')
            val = False
            QMessageBox.critical (self,"Register " , "Password should have at least one lowercase letter" )

        if val:
            return val

    def login (self) :
        user = self.lineEdit.text ()
        passwd = self.lineEdit_2.text ()
        if user and passwd :
            try :
                mycursor.execute("SELECT * FROM login WHERE user = '{}' and pass = '{}' ".format(user , passwd))
                result = (mycursor.fetchall())
                if result == []:
                    mycursor.execute("SELECT * FROM login WHERE user = '{}' ".format(user))
                    user_result = (mycursor.fetchall())
                    if user_result == [] :
                        QMessageBox.critical(self,'Login ','user Not Found ')
                    else :
                        QMessageBox.critical(self,'Login ','password is incorrect')
                
                else: 
                    print(result)
                    QMessageBox.information (self,"Login" , "Login successfull")
                    #هنا هنحط الكود اللي بيودي ل صفحه البرنامج Easy learning 
                    self.hide ()
                    import E2
                    
            except Exception as err :
                QMessageBox.critical(self,'Login ','There is a problem in login')
                print ("error IS : ", err)
        else :
              QMessageBox.critical (self,"Login " , "please Enter user and password to login :)")   

    def create_Acc (self) :
        user = (self.lineEdit_7.text ()).lower() #تحويل النص الى حروف صغيره
        passwd = self.lineEdit_6.text ()
        email = self.lineEdit_5.text ()
        vaild = True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if user and passwd and email :
            print ("check user , email , pass Section")
        #user check - فحص اليوزر
            mycursor.execute("SELECT * FROM login WHERE user = '{}'".format(user))
            result = (mycursor.fetchall())
            if result != []:
                QMessageBox.critical (self,"Register " , "That username is taken. Try another." )
                vaild = False
                self.lineEdit_7.clear ()
        #email check - فحص الايميل 
            mycursor.execute("SELECT * FROM login WHERE email = '{}'".format (email))
            result = (mycursor.fetchall())
            if result != []: 
                QMessageBox.critical (self,"Register " , "That email is taken. Try another." )
                vaild = False
        #فحص صلاحيه الباسوورد
            if (self.password_check(passwd)):
	            print("Password is valid")
            else :
                print ("Invalid Password !!")
                vaild = False
        # فحص صلاحيه الايميل
            if(re.fullmatch(regex, email)):
                print("Valid Email")
            else :
                print("Invalid Email")
                QMessageBox.critical(self,"Register " , "Invalid Email. Try another." )
                vaild = False

            # لو اللي فوق متنفذوش هينفذ اللي تحت هيكريت الأكك
            if vaild == True:
                print ("creat Acc Section")
                 #بيضيف اليوزر و الباص و الايميل
                print("Password is valid")
                mycursor.execute ("insert into login (user,pass,email) Values ('{}','{}','{}')".format(user,passwd,email)) 
                db.commit ()
                self.tabWidget.setCurrentIndex(0)
                QMessageBox.information(self, "Register ", "successfully registered")
        else :
           QMessageBox.critical(self, "Register ", "The data must be entered correctly  ")


    def exit (self) :
        self.close ()
        
    def maximize (self) :
        pass

    def Minimize (self) :
        self.showMinimized()

    def forgetScreen (self) :
        self.tabWidget.setCurrentIndex(1)
    
    def registerScreen (self) :
        self.tabWidget.setCurrentIndex(2)

    def show_pass (self) :
        self.lineEdit_2.setEchoMode(QLineEdit.Normal)
        self.lineEdit_6.setEchoMode(QLineEdit.Normal)
        QtTest.QTest.qWait(1000)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_6.setEchoMode(QLineEdit.Password)

    def mousePressEvent(self, event):
       self.oldPos = event.globalPos() 

    def mouseMoveEvent(self, event ):
       delta = QPoint (event.globalPos() - self.oldPos)
       self.move(self.x() + delta.x(), self.y() + delta.y())
       self.oldPos = event.globalPos() 




app = QApplication(sys.argv)
login  = main()
app.exec_()

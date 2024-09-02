
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import MetaTrader5 as mt5
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import sqlite3

conn=sqlite3.connect('employee.db')
c=conn.cursor()

#create table
try:
    c.execute('''
            CREATE TABLE users(
              Server   text,
              LoginID integer,
              Password  text,
              Suffix   text,
              Symbol text
                )
            ''')
except:
    pass


class home_page(QMainWindow):

    def __init__(self):
        super(home_page,self).__init__()
        loadUi('magicmain.ui',self)
        self.widget=self.stackedWidget
        self.widget.setCurrentWidget(self.home)
        self.mt5btn.clicked.connect(self.mt5_page)
        self.homebtn.clicked.connect(self.home_page)
        self.magicbtn.clicked.connect(self.magic_page)
        self.analyticsbtn.clicked.connect(self.mt_analytics)
   
    ########################### HOME_PAGE ##########################
    def home_page(self):
        self.widget.setCurrentWidget(self.home)
    ########################### Magic PAGE ###########################
    def magic_page(self):
        self.widget.setCurrentWidget(self.magickeys)
        
    ########################### DEFAULTS_PAGE #######################
 
    def mt_analytics(self):
        self.widget.setCurrentWidget(self.mtanalytics)
    ########################### MT5_PAGE   ######################    
    def mt5_page(self):
        self.widget.setCurrentWidget(self.mt)
        self.mtaddbtn.clicked.connect(self.line_data)
        self.mtshow.clicked.connect(self.show_accounts)
        self.mtlogin.clicked.connect(self.login_accounts)
        self.mtdelete.clicked.connect(self.delete_accounts)
    def login_accounts(self):
        mt5.initialize()
        items = self.mtlist.selectedItems()
        for i in range(len(items)):
            self.ID=self.mtlist.selectedItems()[i].text().split(':')
            c.execute('SELECT * FROM users WHERE LoginID =:ID',{'ID':int(self.ID[1])})
            data=c.fetchall()
            for mt in data:
                server=mt[0]
                logins=mt[1]
                password=mt[2]
                mt5.login(logins,password,server)
    def delete_accounts(self):
        items = self.mtlist.selectedItems()
        for i in range(len(items)):
            self.ID=self.mtlist.selectedItems()[i].text().split(':')
            c.execute('DELETE FROM users WHERE LoginID =:ID',{'ID':int(self.ID[1])})
            conn.commit()  
            self.show_accounts()
            #self.error.setText('please select the ID row!')
    def show_accounts(self):
        self.mtlist.clear()
        c.execute("SELECT * FROM users")
        data=c.fetchall()
        for mt in data:
            #self.mtlist.addItem(str(mt))
            self.mtlist.addItem(str(f'server : {mt[0]}'))
            self.mtlist.addItem(str(f'ID : {mt[1]}'))
            self.mtlist.addItem(str(f'Suffix : {mt[3]}'))
            self.mtlist.addItem(str(f'Symbols : {mt[4]}'))
            self.mtlist.addItem(str('............................. '))
    def line_data(self):
        
        mtserver=self.mtserver.text()
        if not mtserver:
            self.serverError.setText('* Required')
        mtid=self.mtid.text()
        if not mtid:
            self.idError.setText('* Required')
        mtpass=self.mtpassword.text()
        if not mtpass:
            self.passError.setText('* Required')
        mtsuffix=self.mtsuffix.text()
        mtsymbol=self.mtsymbols.text()
        if mtserver and mtpass and mtid:
            c.execute("INSERT INTO users VALUES(:server,:login,:pass,:suffix,:symbol)",{'server':mtserver,'login':mtid,'pass':mtpass,'suffix':mtsuffix,'symbol':mtsymbol})
            conn.commit()
        self.mtserver.clear()
        self.mtid.clear()
        self.mtpassword.clear()
        self.mtsuffix.clear()
        self.mtsymbols.clear()

    def add_item(self):
        self.error.setText('')  
        items = self.list1.selectedItems()
        for i in range(len(items)):
            itemsTextList =  [str(self.list2.item(i).text()) for i in range(self.list2.count())]
            if self.list1.selectedItems()[i].text() in itemsTextList:
                self.error.setText('--> Duplicates not allowed!')
                #print('its duplicate')
                continue
            else:
                #('added',self.list1.selectedItems()[i].text())
                #row=self.list2.count()+1
                self.list2.addItem(str(self.list1.selectedItems()[i].text()))
                #self.list2.insertItem(row,str(self.list1.selectedItems()[i].text()))
                #self.list2.addItem(str(self.list1.selectedItems()[i].text()))
                
    def remove_item(self):
        #self.list2.removeItemWidget(self.list2.selectedItems()[i])
        self.list2.takeItem(self.list2.currentRow())
    def save_item(self):
        itemsTextList =  [str(self.list2.item(i).text()) for i in range(self.list2.count())]        
        
        with open("alljang.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(itemsTextList) 
        
        print('done')
    #######################################################################
    


app=QApplication(sys.argv)
home=home_page()

#stacked widget is for moving between screens
widget = QtWidgets.QStackedWidget()
widget.setMinimumHeight(620)
widget.setMinimumWidth(1000)
widget.addWidget(home)
widget.setCurrentIndex(widget.currentIndex()+1)
widget.show()

try:
    sys.exit(app.exec())
except:
    print('there is a problem')


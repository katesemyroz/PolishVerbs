# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide.QtCore import *
import sys
import sqlite3
import os
import random
import csv
import time

import polishVerbsGui

appDataPath = os.environ["APPDATA"] + "\\PolishVerbs\\"

if not os.path.exists(appDataPath):
    try:
        os.makedirs(appDataPath)
    except Exception, e:
        appDataPath = os.getcwd()


class Main(QMainWindow, polishVerbsGui.Ui_MainWindow):

    dbPath = appDataPath + "pydata.db"
    dbConn = sqlite3.connect(dbPath)
    dbConn.text_factory = str

    #variable which counts how much right answers the user have
    number_of_right_answers = 0
    can_take_point = True

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.dbCursor = self.dbConn.cursor()
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Main(id INTEGER PRIMARY KEY,
                              verb TEXT, ja TEXT, ty TEXT, on_ona_ono TEXT,
                              my TEXT, wy TEXT, oni_one TEXT)""")
        self.dbConn.commit()
        self.fill_database()

        self.new_verb_button_clicked()
        self.new_verb_button.clicked.connect(self.new_verb_button_clicked)
        self.check_button.clicked.connect(self.check_button_clicked)
        self.show_answers_button.clicked.connect(self.show_answers_button_clicked)


    def test_form(self):
        """
        Test methods with 3 correct forms and 3 incorrect
        """

        self.verb.setText("być".decode("utf-8"))
        self.ja.setText("j".decode("utf-8"))
        self.ty.setText("jesteś".decode("utf-8"))
        self.on_ona_ono.setText("jest".decode("utf-8"))
        self.my.setText("jeeeeemmmmmyyy".decode("utf-8"))
        self.wy.setText("jesteście".decode("utf-8"))
        self.oni_one.setText("saaaaaaa".decode("utf-8"))

    def test_form_right_answers(self):
        """
        Test methods with all correct forms
        """

        self.verb.setText("być".decode("utf-8"))
        self.ja.setText("jestem".decode("utf-8"))
        self.ty.setText("jesteś".decode("utf-8"))
        self.on_ona_ono.setText("jest".decode("utf-8"))
        self.my.setText("jesteśmy".decode("utf-8"))
        self.wy.setText("jesteście".decode("utf-8"))
        self.oni_one.setText("są".decode("utf-8"))

    def fill_database(self):
        """
        This function checks if there are words in database. If no - fills it from verbs.csv file
        """

        self.dbCursor.execute("""SELECT count(verb) FROM Main""")
        number_of_verbs = self.dbCursor.fetchone()
        if (number_of_verbs[0] == 0):
            with open("verbs_and_forms.csv", 'rb') as resultFile:
                reader = csv.reader(resultFile)
                for row in reader:
                    self.dbCursor.execute('''INSERT INTO Main VALUES (null, ?, ?, ?, ?, ?, ?, ?)''', row)
                self.dbConn.commit()
        else:
            pass

    def new_verb_button_clicked(self):
        """
        Change the Verb in the top of application and clear all the information that was
        entered by the user before
        """

        self.dbCursor.execute("""SELECT count(verb) FROM Main""")
        number_of_verbs = self.dbCursor.fetchone()
        id_of_random_verb = random.randint(1, number_of_verbs[0])
        self.dbCursor.execute("""SELECT verb FROM Main WHERE id=?""", (id_of_random_verb,))
        random_verb = self.dbCursor.fetchone()
        random_verb_unicode = random_verb[0].decode('utf-8')
        self.verb.setText(random_verb_unicode)
        all_line_edit_fields = (self.ja, self.ty, self.on_ona_ono, self.my, self.wy, self.oni_one)
        for field in all_line_edit_fields:
            field.clear()
            field.setStyleSheet("""border: 2px solid #8c7aae; border-style: outset;
            border-radius: 3px; background-color: white""")
        self.can_take_point = True

    def check_button_clicked(self):
        """
        Check if all the fields are written in the right way
        by comparing meaning with information in database.
        Paint the correct fields in green, wrong fields in red.
        If all fields are correct - number of right answers increase
        """

        all_line_edit_fields = (self.ja, self.ty, self.on_ona_ono, self.my, self.wy, self.oni_one)
        right_answers = 0
        current_verb = self.verb.text().encode('utf-8')
        #print current_verb, type(current_verb)
        self.dbCursor.execute('SELECT * FROM Main WHERE verb=?', (current_verb,))
        allForms = self.dbCursor.fetchall()
        for form in allForms:
            for x in range(2, 8):
                this_line_edit = all_line_edit_fields[x-2]
                what_user_enters = this_line_edit.text().encode('utf-8')
                if form[x] == what_user_enters:
                    right_answers += 1
                    this_line_edit.setStyleSheet("""border: 2px solid #00c322; border-style: outset;
                    border-radius: 3px; background-color: white""")
                else:
                    this_line_edit.setStyleSheet("""border: 2px solid #ff3300; border-style: outset;
                    border-radius: 3px; background-color: white""")

        if right_answers == 6:
            if self.can_take_point:
                self.number_of_right_answers += 1
                self.label_with_result.setText(`self.number_of_right_answers`)
                self.can_take_point = False
            else:
                pass

    def show_answers_button_clicked(self):
        """
        Shows right answers, paint all fields in red
        """
        all_line_edit_fields = (self.ja, self.ty, self.on_ona_ono, self.my, self.wy, self.oni_one)
        current_verb = self.verb.text().encode('utf-8')
        self.dbCursor.execute('SELECT * FROM Main WHERE verb=?', (current_verb,))
        allForms = self.dbCursor.fetchall()
        for form in allForms:
            for x in range(2, 8):
                all_line_edit_fields[x-2].setText(form[x].decode("utf-8"))
                all_line_edit_fields[x-2].setStyleSheet("""border: 2px solid #00c322; border-style: outset;
                    border-radius: 3px; background-color: white""")
        self.can_take_point = False





def main():
    QCoreApplication.setApplicationName("PolishVerbs")
    QCoreApplication.setApplicationVersion("0.2")
    QCoreApplication.setOrganizationName("Kate Semyroz")

    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()


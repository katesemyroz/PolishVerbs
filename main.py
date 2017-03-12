from PySide.QtGui import *
from PySide.QtCore import *
import sys
import re
import sqlite3
import os
import logging
import random

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

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.dbCursor = self.dbConn.cursor()
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Main(id INTEGER PRIMARY KEY,
                              verb TEXT, ja TEXT, ty TEXT, on_ona_ono TEXT,
                              my TEXT, wy TEXT, oni_one TEXT)""")
        self.dbConn.commit()


        self.dbCursor.execute("""SELECT count(verb) FROM Main""")
        number_of_verbs = self.dbCursor.fetchone()
        id_of_random_verb = random.randint(1, number_of_verbs[0])
        self.dbCursor.execute("""SELECT verb FROM Main WHERE id=?""", (id_of_random_verb,))
        random_verb = self.dbCursor.fetchone()
        print random_verb[0]
        self.verb.setText(random_verb[0])

        self.check_button.clicked.connect(self.check_button_clicked)



    def check_button_clicked(self):
        """Paint the correct fields in green, paint wrong fields in red.
            If all fields are correct - write text 'Everything is correct', else - 'You
            have n correct answers' or 'Everything is wrong! Try again' """


        all_line_edit_fields = (self.ja, self.ty, self.on_ona_ono, self.my, self.wy, self.oni_one)
        right_answers = 0
        current_verb = self.verb.text().encode('utf-8')
        self.dbCursor.execute('SELECT * FROM Main WHERE verb=?', (current_verb,))
        allForms = self.dbCursor.fetchall()
        for form in allForms:
            for x in range(2, 8):
                this_line_edit = all_line_edit_fields[x-2]
                what_user_enters = this_line_edit.text().encode('utf-8')
                if form[x] == what_user_enters:
                    right_answers += 1
                    this_line_edit.setStyleSheet("selection-background-color: green; background-color: green")
                else:
                    this_line_edit.setStyleSheet("selection-background-color: red; background-color: red")


        print right_answers
        if right_answers == 6:
            print "Everything is correct!"
        else:
            if right_answers == 0:
                print "Everything is wrong! Try again"
            else:
                print "You have", right_answers, "right answers"


    def check_fields(self):
        """Check if all the fields are written in the right way or
           in the wrong way by comparing meaning with information in
           database"""
        pass


def main():
    QCoreApplication.setApplicationName("PolishVerbs")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("KS")

    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()


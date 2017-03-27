# -*- coding: utf-8 -*-
__author__ = 'pc'

import sys
import unittest
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtTest import *
from main import *
import sqlite3


class TestMain(unittest.TestCase):
    def test_check_button_clicked(self):
        self.app = QApplication([])
        #self.fail()
        m = Main()
        m.verb.setText("Mam")
        test_line_edit_fields = ("mam", "masz", "ma", "mamy", "macie", "mają")
        all_line_edit_fields = (m.ja, m.ty, m.on_ona_ono, m.my, m.wy, m.oni_one)
        for x in xrange(6):
            all_line_edit_fields[x].setText(test_line_edit_fields[x])
        self.assertEqual(m.ja.text(), "mam")
        m.check_button_clicked()
        self.assertEqual(m.number_of_right_answers, 1)



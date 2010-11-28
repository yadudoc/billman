#!/usr/bin/python
__author__ = 'yadudoc1729@gmail.com (Yadu Nand B)'

import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore


import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore


class InputDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #self.setGeometry(300, 300, 350, 80)

        
        self.setWindowTitle('InputDialog')
        self.resize(250, 100)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        # Reading Username
        label = QtGui.QLabel('Username',self);
        label.move(20,10)
        self.label1 = QtGui.QLineEdit(self)
        self.label1.move(100, 10)

        # Reading Password
        label = QtGui.QLabel('Password',self);
        label.move(20,40)
        self.label2 = QtGui.QLineEdit(self)
        self.label2.move(100, 40)

        # Sync button
        self.button = QtGui.QPushButton('Sync', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(150, 70)
        

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.setFocus()
        
        
        
    def showDialog(self):
       # text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')              
        self.label1.setText("Done!")
        self.label2.setText(self.label1.text())
    

            

app = QtGui.QApplication(sys.argv)
idlg = InputDialog()
idlg.show()
app.exec_()

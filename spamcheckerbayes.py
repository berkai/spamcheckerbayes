#  -*- coding:utf-8 -*-
# import libraries for front end
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QLabel
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory, QLineEdit, QInputDialog
#import libraries for analysiş
import os
import io
import numpy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class window(QMainWindow):

    def __init__(self):
        '''
        main window  function
        '''
        super(window, self).__init__()
        self.setGeometry(50, 50, 350, 350)#set display screen properties
        self.setWindowTitle('SPAM Check')

        #extract train file
        extractAction = QAction('&Exit', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Exit the app')
        extractAction.triggered.connect(self.close_application)

        #this text will be analyze
        self.getTextbox = QLineEdit(self, placeholderText="Enter the text.")
        self.getTextbox.move(20, 50)
        self.getTextbox.resize(280,40)

        #this is will be threshold
        self.getThreshold = QLineEdit(self, placeholderText="Threshold value.")
        self.getThreshold.move(20, 100)
        self.getThreshold.resize(280,40)

        #this label show the result spam or ham
        self.resultLabel = QLabel(self)
        self.resultLabel.setText("Result")
        self.resultLabel.move(20,200)

        #when the clicked button resultLabel will be change
        resultBtn = QPushButton('Show Result', self)
        resultBtn.resize(resultBtn.sizeHint())
        resultBtn.clicked.connect(self.showResult)
        resultBtn.move(90, 200)

        #pick the file dialog will be open 
        openFile = QAction('&Upload Train file', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Pick the file')
        openFile.triggered.connect(self.file_open)

        #menubar add
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Train File')
        fileMenu.addAction(extractAction)

        fileMenu.addAction(openFile)

        self.home()
    def file_open(self):
        '''
        pick the file and save the datapath variable
        '''
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        file = open(name, 'r')
        self.data = pd.read_csv(file)     
    @pyqtSlot()
    def showResult(self):
        '''
        Bayes calculation and update the resultLabel changing
        '''
        vectorizer = CountVectorizer()
        counts = vectorizer.fit_transform(self.data['message'].values) #vectorize the mail
        classifier = MultinomialNB()
        targets = self.data['label'].values #get the labels
        classifier.fit(counts, targets) # fit the data
        self.testText = [f'{self.getTextbox.text()}']
        self.testCount = vectorizer.transform(self.testText)
        self.predictions = classifier.predict(self.testCount)
        self.resultLabel.setText(f"{self.predictions}")
    def home(self):
        '''
        Exit button function
        '''
        btn = QPushButton('Exit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())
        btn.move(200, 200)
        self.show()
    def close_application(self):
        '''
        if you pressed the exit button this dialog will be open
        '''
        choice = QMessageBox.question(self, 'Message',
                                     "Are you sure?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('log out')
            sys.exit()
        else:
            pass

if __name__ == "__main__":  # had to add this otherwise app crashed
    def run():
        app = QApplication(sys.argv)
        Gui = window()
        sys.exit(app.exec_())
run()
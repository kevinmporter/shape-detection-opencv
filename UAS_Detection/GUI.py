import sys
import PyQt4
from PyQt4 import QtGui
import cv2
import numpy as np
import Detection
import os
import sys


class GUI(QtGui.QWidget):
    filepath = 'ScreenCaptureProject4.avi'
    flag = False
    def __init__(self):
        super(GUI, self).__init__()

        self.initUI()

    def initUI(self):

        lbl = QtGui.QLabel('Video to Process:', self)
        lbl.move(60, 60)
        btn = QtGui.QPushButton('Browse', self)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.SingleBrowse)
        btn.move(170, 55)
        btn2 = QtGui.QPushButton('Detect', self)
        btn2.resize(btn.sizeHint())
        btn2.clicked.connect(self.SingleDetect)
        btn2.move(230, 90)

        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Search and Response Software')
        self.show()

    def SingleDetect(self):
        os.system('python Detection.py')


    def setFileName(self, x):

        filepath = x

    def getFileName(self):
        return self.filepath

    def SingleBrowse(self):
        filePaths = QtGui.QFileDialog.getOpenFileNames(self,
                                                       'Multiple File',
                                                       "~/Desktop/PyRevolution/PyQt4",
                                                      '*.avi')
        for filePath in filePaths:
            print('filePath',filePath, '\n')
            fileHandle = open(filePath, 'r')
            lines = fileHandle.readlines()
            for line in lines:
                print("File Path ->" + line)
                self.setFileName(line)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

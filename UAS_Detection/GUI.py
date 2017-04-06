"""
The GUI configuration in order to interface with Detection.py. Gives the user
the opportunity to supply a path and to begin detection.
"""
import sys
try:
    import PyQt4
    from PyQt4 import QtGui
except ImportError:
    print 'PyQt4 is required to run this GUI software. Please install PyQt4 or ' + \
        'run Detection.py directly to use in CLI mode.'
import cv2
import numpy as np
import Detection
import os
import sys
import subprocess


class GUI(QtGui.QWidget):
    """
    PyQt4 window.
    """
    filepath = None

    flag = False
    def __init__(self):
        super(GUI, self).__init__()
        self.initUI()

    def initUI(self):
        """
        Configure the system with all the requisite buttons.
        :return: nothing
        """

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
        """
        Call Detection.py.
        :return: nothing
        """
        print "SingleDetect " + GUI.filepath
        subprocess.call(['python', 'Detection.py', str(GUI.filepath)])

    def SingleBrowse(self):
        """
        Browse for a video file to run detection on.
        :return: nothing
        """
        filePaths = QtGui.QFileDialog.getOpenFileNames(self,
                                                       'Multiple File',
                                                       "~/Desktop/PyRevolution/PyQt4",
                                                      '*.avi')
        for path in filePaths:
            print('filePath',path, '\n')
            fileHandle = open(path, 'r')
            #lines = fileHandle.readlines()
            print("File Path -> " + fileHandle.name)
            GUI.filepath = fileHandle.name



def main():
    app = QtGui.QApplication(sys.argv)
    ex = GUI()
    print "in GUI main"
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

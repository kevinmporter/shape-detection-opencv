from subprocess import call
from threading import Thread
import numpy as np
import cv2
import datetime
import os
from PyQt4 import QtGui
import sys
import GUI

def pull_key_frames(path):
    os.system('/usr/local/bin/ffmpeg -i ' + path + ' -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 tmp/%d.jpeg')



def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness=1):
    for x, y, w, h in rects:
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    thread = Thread(target=pull_key_frames, args=(GUI.GUI.filepath, ))
    thread.start()
    num = 1
    while True:
        path = os.path.join('tmp', str(num) + '.jpeg')
        if os.path.isfile(path):
            num += 1
            frame = cv2.imread(path)
            print datetime.datetime.now()
            found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
            draw_detections(frame, found)
            cv2.imshow('feed', frame)
            ch = 0xFF & cv2.waitKey(1)
            if ch == 27:
                break
    cv2.destroyAllWindows()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

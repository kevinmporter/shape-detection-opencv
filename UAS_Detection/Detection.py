from subprocess import call
from threading import Thread
import numpy as np
import cv2
import datetime
import os
try:
    from PyQt4 import QtGui
    import GUI
except ImportError:
    pass
from db import Result, VideoRun
import sys
import shutil


record = VideoRun()
results = []


def pull_key_frames(path):
    os.system('ffmpeg -i ' + path + ' -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 tmp/%d.jpeg')
    record.end = datetime.datetime.now()
    record.results = results
    record.save()


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness=1):
    for x, y, w, h in rects:
        result = Result(picture=img, x=x, y=y, w=w, h=h)
        result.save()
        results.append(result)
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    # get the human object detection module
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    thread = Thread(target=pull_key_frames, args=(sys.argv[1],))
    # begin extracting the keyframes from the video file in a separate thread
    thread.start()
    start = datetime.datetime.now()
    record.start = start
    num = 1
    #print("In Detection main "+"File Path ->" + sys.argv[1])
    # look for new frames in the tmp directory
    while True:
        path = os.path.join('tmp', str(num) + '.jpeg')
        if os.path.isfile(path):  # if the file exists
            num += 1
            frame = cv2.imread(path)
            print datetime.datetime.now()
            # on the frame, get the dimensions surrounding a "found" object
            found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
            # draw a rectangle around it
            draw_detections(frame, found)
            # display to user
            cv2.imshow('feed', frame)
            ch = 0xFF & cv2.waitKey(1)
            if ch == 27:
                break
    shutil.rmtree('tmp', ignore_errors=True)
    cv2.destroyAllWindows()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


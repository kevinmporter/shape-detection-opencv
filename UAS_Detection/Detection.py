"""
Shape detection algorithm using OpenCV. Assumes the presence of database
file. Uses multithreading capability in order to run ffmpeg in the background to
simultaneously pull keyframes from the image while processing the frames.
"""
from threading import Thread
import numpy as np
import cv2
import datetime
import os
import db
import sys
import shutil
import time
try:
    from PyQt4 import QtGui
    import GUI
except ImportError:
    # CLI only
    print 'This software requires PyQt4. Switching to CLI mode.\n'


record = db.VideoRun()
results = []


def pull_key_frames(path):
    """
    Run ffmpeg against the supplied path in order to get the keyframes back.
    :param path: a path to a video file
    :return: nothing
    """
    os.system('ffmpeg -i ' + path + ' -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 tmp/%d.jpeg')
    record.end = datetime.datetime.now()


def inside(r, q):
    """
    
    :param r: 
    :param q: 
    :return: 
    """
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, imgpath, thickness=1):
    """
    Draws a rectangle around the supplied dimensions and saves the record.
    :param img: the frame from OpenCV
    :param rects: the rectangles in this frame to draw, each with x, y, w, h
    :param imgpath: the path to the image frame itself
    :param thickness: the thickness of the rectangle line to draw
    :return: nothing
    """
    with open(imgpath, 'rb') as f:
        for x, y, w, h in rects:
            result = db.Result(x=x, y=y, w=w, h=h)
            result.picture.put(f)
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
    time.sleep(5)  # wait for ffmpeg to start
    # look for new frames in the tmp directory
    while True:
        path = os.path.join('tmp', str(num) + '.jpeg')
        if os.path.isfile(path) or thread.isAlive():  # if the file exists
            if os.path.isfile(path):
                num += 1
                frame = cv2.imread(path)
                # on the frame, get the dimensions surrounding a "found" object
                found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
                # draw a rectangle around it
                draw_detections(frame, found, path)
                # display to user
                cv2.imshow('feed', frame)
                ch = 0xFF & cv2.waitKey(1)
                if ch == 27:
                    break
        else:
            break
    record.results = results
    record.save()
    shutil.rmtree('tmp', ignore_errors=True)
    cv2.destroyAllWindows()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

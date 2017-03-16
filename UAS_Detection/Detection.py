from subprocess import call
from threading import Thread
import numpy as np
import cv2
import datetime


def pull_key_frames(path, flag):
    flag = True
    call('ffmpeg -i ' + path + ' -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 tmp/thumbnails-%02d.jpeg')
    flag = False

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real
        #  objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    cap = cv2.VideoCapture('/Users/porterkm/Projects/shape-detection-opencv/UAS_Detection/dumb.mp4')
    '''
    ffmpeg -i dumb.mp4 -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 tmp/thumbnails-%02d.jpeg
    '''
    flag = True
    pull_key_frames('dumb.mp4', flag)
    while flag:
        _, frame = cap.read()
        print datetime.datetime.now()
        found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
        draw_detections(frame, found)
        cv2.imshow('feed', frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cv2.destroyAllWindows()

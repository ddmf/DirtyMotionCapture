from datetime import datetime
import cv2
import ntpath
import os

CONST_ROOTPATH = "c:\\video\\"

def path_filename(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

def DetectMotion(filename):
    filenameonly = path_filename(filename)
    print filenameonly
    cam = cv2.VideoCapture(filename)
    
    #populate initial images
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = t_minus
    t_plus = t_minus
    frame=0
    
    while(cam.isOpened()):
        t_minus=t
        t=t_plus
        img=cam.read()[1]
        if (type(img) == type(None)):
            break
    
        t_plus=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        diff=diffImg(t_minus,t,t_plus)
        nz=cv2.countNonZero(diff)
        if nz>12000:
            cv2.imwrite('{0}\\images\\{1}-{2:06d}.jpg'.format(CONST_ROOTPATH,filenameonly,frame), img)
            #cv2.imwrite('{0}\\images\\{1}-{2:06d}-{3:06d}.jpg'.format(CONST_ROOTPATH,filenameonly,frame,nz), diff)
        frame+=1
            
    cam.release()


for file in os.listdir(CONST_ROOTPATH):
    if file.endswith(".avi"):
        DetectMotion(file)

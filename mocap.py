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
    ma=0
    
    while(cam.isOpened()):
        t_minus=t
        t=t_plus
        img=cam.read()[1]
        if (type(img) == type(None)):
            break
    
        t_plus=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        diff=diffImg(t_minus,t,t_plus)
        cv2.threshold(diff,127,255,cv2.THRESH_BINARY,diff)            
        nz=cv2.countNonZero(diff)
        ma=(ma+nz)/2
        if nz>0:
            pc=(abs(nz-ma)/float(nz))
        else:
            pc=0
        if (nz>4) and (pc>0.2):
            #print '{0:06d} {1} {2} {3:.4f}'.format(frame,nz,ma,pc)
            cv2.imwrite('{0}\\image\\{1}-{2:06d}.jpg'.format(CONST_ROOTPATH,filenameonly,frame), img)
            #cv2.imwrite('{0}\\image\\{1}-{2:06d}-Diff{3:06d}-MA{4:06}.jpg'.format(CONST_ROOTPATH,filenameonly,frame,nz,ma), diff)
        frame+=1
            
    cam.release()


for file in os.listdir(CONST_ROOTPATH):
    if file.endswith(".avi"):
        DetectMotion(file)

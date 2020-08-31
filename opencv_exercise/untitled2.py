# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 11:05:34 2020

@author: a0970
"""


'''
s_img = cv2.imread("smaller_image.png", -1)


'''
import cv2

def convert_image(source):
# 脸
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_cascade.load('sources/data/haarcascades/haarcascade_frontalface_default.xml')
# 眼睛
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    eye_cascade.load('sources/data/haarcascades/haarcascade_eye.xml')
#嘴巴
    mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    mouth_cascade.load('sources/data/haarcascades/haarcascade_smile.xml')

 
#face_cascade = cv2.CascadeClassifier("../../opencv-2.4.9/data/haarcascades/haarcascade_frontalface_default.xml")  
#eye_cascade = cv2.CascadeClassifier('../../opencv-2.4.9/data/haarcascades/haarcascade_eye.xml')  

    img = cv2.imread(source + '.jpg')
    img_in = cv2.imread('mask.png',-1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#脸
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)
    for (x, y, w, h) in faces:
         x_offset = [];
         y_offset = [];

         #img = cv2.rectangle(img, (x,y),(x+w, y+h), (255, 0, 0), 2)
         roi_gray = gray[y:y+h, x:x+w]
         print('face:',x,y,w,h)
     #嘴巴
         mouth = mouth_cascade.detectMultiScale(roi_gray, 1.5,5)
         for (ex,ey,ew,eh) in mouth:
             #cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
             print('mouth:',ex,ey,ew,eh)
             x_offset.append(ex)
             y_offset.append(ey)
             print('offset',x_offset,y_offset)
         if len(x_offset) > 0:
             img_in = cv2.resize(img_in, (int(h*0.5), int(h*0.5)))
             Index = y_offset.index(max(y_offset))
             #for i in range(0,len(y_offset)) :
             y1, y2 = max(y_offset), max(y_offset) + img_in.shape[0]
             x1, x2 = x_offset[Index], x_offset[Index] + img_in.shape[1]
             alpha_s = img_in[:, :, 3] / 255.0
             alpha_l = 1.0 - alpha_s
             move_x = x - 10
             move_y = y - int(h*0.5*0.5)
         for c in range(0, 3):
             img[y1 + move_y:y2 + move_y, x1 + move_x:x2 + move_x, c] = (alpha_s * img_in[:, :, c] +
                              alpha_l * img[y1 + move_y:y2 + move_y, x1 + move_x:x2 + move_x, c])
#cv2.imshow('img', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
    cv2.imwrite(source + '_converted.jpg',img)
    return source + '_converted.jpg'

print(convert_image('human2'))
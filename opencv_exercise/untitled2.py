# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 11:05:34 2020

@author: a0970
"""



#img = Image.open("lena.jpg")
#print(img.size)
#img2 = Image.open("lena-thumbnail.jpg")
#print(img2.size)
#img.thumbnail((256, 256))
#img.paste(img2, (150, 50))
#img.show()

from PIL import Image
import numpy as np
import cv2

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

img = cv2.imread('human2.jpg')
#img_out = Image.open('human.jpg')
#img_in = Image.open('mask.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img_in.thumbnail((256, 256))

#脸
faces = face_cascade.detectMultiScale(gray, 1.2, 3)
for (x, y, w, h) in faces:
     img = cv2.rectangle(img, (x,y),(x+w, y+h), (255, 0, 0), 2)
     roi_gray = gray[y:y+h, x:x+w]
     roi_color = img[y:y+h, x:x+w]
     print('face:',x,y,w,h)
     #眼睛
     eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 3)
     for (ex,ey,ew,eh) in eyes:
          cv2.rectangle(roi_color, (ex, ey),(ex+ew, ey+eh), (0, 255, 0), 2)
          print('eyes:',ex,ey,ew,eh)
     #嘴巴
     mouth = mouth_cascade.detectMultiScale(roi_gray, 1.5,5)
     for (ex,ey,ew,eh) in mouth:
         cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
         print('mouth:',ex,ey,ew,eh)
         #center = (ex + int(0.5*ew) + 128,int(ey + 0.5*eh) + 128)
     #print(mouth)
#print(center)        
#img_out.paste(img_in, center)
cv2.imshow('img', img)
#img_out.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

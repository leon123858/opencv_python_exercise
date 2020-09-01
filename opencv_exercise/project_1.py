# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 11:45:44 2020

@author: a0970
"""

from flask import Flask
app = Flask(__name__)

from flask import abort
from flask import Flask, request , Response
#from mask_cov import  convert_image
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction,ImageMessage

line_bot_api = LineBotApi('xfbswSOGDiTYobcg3N189Dc2ADxreb8Fv1MshiH42fMpCyCzyIl02cerdXehEAIVjVB/EBJoXXlXdQJmTvcpjSSd1FVL48zIT+PQYxi/vtLlG6dve94Lwd9Z0voEln34kTrqPeKBK3pUd1X0XiNWPQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('34a1c3fdd183102a004ded05c0dc3811')




#mask_cover_fun


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
        x_offset = []
        y_offset = []

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
            img_in = cv2.resize(img_in, (int(h*0.5), int(h*0.6)))
            Index = y_offset.index(max(y_offset))
            #for i in range(0,len(y_offset)) : 
            y1, y2 = max(y_offset), max(y_offset) + img_in.shape[0]
            x1, x2 = x_offset[Index], x_offset[Index] + img_in.shape[1]
            alpha_s = img_in[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            move_x = x - 10
            move_y = y - int(h*0.5*0.5)
        
        for c in range(0, 3):
            img[y1 + move_y:y2 + move_y, x1 + move_x:x2 + move_x, c] = (alpha_s * img_in[:, :, c] + alpha_l * img[y1 + move_y:y2 + move_y, x1 + move_x:x2 + move_x, c])

#cv2.imshow('img', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
    cv2.imwrite(source + '_converted.jpg',img)
    return source + '_converted.jpg'





@app.route("/image", methods=['post', 'get'])
def index():
    path = request.args.get('path')
    print(path)
    path =  path
    try :
        resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    except InvalidSignatureError:
        abort(400) 
    return resp



@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#加入一個message handler
#XXXXXXXX


@handler.add(MessageEvent ,message=ImageMessage)
def handle_message_image(event):
        ext = '.jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(event.message.id + ext,'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
    
        reimg=convert_image(event.message.id)
        reimg = 'https://7ab75a946a8a.ngrok.io/image?path=' + reimg
        print(reimg)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage( original_content_url =reimg , preview_image_url = reimg))
    
 



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == 'Hi':
        try:
            message = TextSendMessage(text = "Hi, I am Mask-App.")
            line_bot_api.reply_message(event.reply_token , message)
        except:
            line_bot_api.reply_message(event.reply_token , TextSendMessage(text='Please try again,thx.'))
            
            
    elif mtext == '來看精選口罩！':
            uri = 'https://7ab75a946a8a.ngrok.io/image?path='
            message = [
                #ImageSendMessage( 
                #class
                #original_content_url ='https://i.imgur.com/CSQJsZP.jpg',
                #preview_image_url = 'https://i.imgur.com/CSQJsZP.jpg'),
                
                ImageSendMessage(
                #original
                original_content_url =uri + '12601132093474.jpg_converted.jpg',
                preview_image_url = uri + '12601132093474.jpg_converted.jpg'),
                
                 ImageSendMessage(
                #original
                original_content_url = uri +'12601136402499.jpg_converted.jpg',
                preview_image_url = uri + '12601136402499.jpg_converted.jpg'),
                 
                 ImageSendMessage(
                #original
                original_content_url =uri+'12601138680722.jpg_converted.jpg',
                preview_image_url = uri+'12601138680722.jpg_converted.jpg'),
                 
                 ImageSendMessage(
                #original
                original_content_url =uri+'12601141694399.jpg_converted.jpg',
                preview_image_url =uri+ '12601141694399.jpg_converted.jpg')
                 
            ]
            line_bot_api.reply_message(event.reply_token , message)
            
    elif mtext == '貼圖':
        try:
            message = StickerSendMessage( 
                package_id = '1', 
                sticker_id = '410'
            )
            line_bot_api.reply_message(event.reply_token , message)
        except:
            line_bot_api.reply_message(event.reply_token , TextSendMessage(text='Please try again,thx.'))
            
    elif mtext == '多項傳送':
        try:
            message = [
                StickerSendMessage( 
                    package_id = '1', 
                    sticker_id = '410'
                ),
                TextSendMessage(text = "Hi, I am Mask-App."),
                
                ImageSendMessage( 
                    original_content_url ='https://i.imgur.com/CSQJsZP.jpg' , 
                    preview_image_url = 'https://i.imgur.com/CSQJsZP.jpg'
                )
            ]
            
            line_bot_api.reply_message(event.reply_token , message)
        except:
            line_bot_api.reply_message(event.reply_token , TextSendMessage(text='Please try again,thx.'))
            
    
    elif mtext == '位置':
        try:
            message = LocationSendMessage( 
                title = '交通大學 台南分校',
                address = '台南市歸仁區高發三路301號',
                latitude=22.924879,
                longitude=120.294950
            )
            line_bot_api.reply_message(event.reply_token , message)
        except:
            line_bot_api.reply_message(event.reply_token , TextSendMessage(text='Please try again,thx.'))
            
    elif mtext == '快速選單':
        try:
            message = TextSendMessage( 
                text = 'please select',
                quick_reply = QuickReply(
                    items=[
                        QuickReplyButton(action = MessageAction(label = "文字" , text = "文字")),
                        QuickReplyButton(action = MessageAction(label = "圖片" , text = "圖片")),
                        QuickReplyButton(action = MessageAction(label = "貼圖" , text = "貼圖")),
                        QuickReplyButton(action = MessageAction(label = "多項傳送" , text = "多項傳送")),
                        QuickReplyButton(action = MessageAction(label = "位置" , text = "位置")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token , message)
        except:
            line_bot_api.reply_message(event.reply_token , TextSendMessage(text='Please try again,thx.'))



    
    
    

    
    

   
    
    
    
    
if __name__ == '__main__':
    app.run()
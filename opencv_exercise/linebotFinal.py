# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 16:05:45 2020

@author: a0970
"""

from flask import Flask
app = Flask(__name__)
#引用自己寫的物件
from linebot_function.invoice import invoice
from flask import Flask, request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction,ImageMessage

line_bot_api = LineBotApi('5rpf/HRRLIjyu6T5br1CXWLFaxwMY4w8cy1v50nhKmLEOMoVou9c9IwNSeNa32jWPMq5kYFqGk7FJm4Aa3oRosS3PbqbTQntCfWT5kKgj1gyeQ2eO0kDSg8W0VuCZT00whYjDzP359hpzduP95KSlwdB04t89/1O/w1cDnyilFU=/7oJVEqzz8kVG4Dwwem6V+KCeoAS2cG9I7yprBYxVk24YYBw53Vy1PfJ2Rq71wgUoU5x2fiBWXhIfgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5b059db759e4dfa3b5a44c2896faed21')


def is_threeDigit_int(number):
    if number.isdigit() :
        if len(number) == 3:
            return True
        else:
            return False
    else:
        return False

@app.route("/", methods=['POST'])
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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Invoice = invoice('https://invoice.etax.nat.gov.tw/invoice.xml')
        img_url = 'https://i.imgur.com/4Ze2vH4.jpg';
        if event.message.text == '我要妹':
            mtext = ImageSendMessage(original_content_url=img_url,preview_image_url=img_url)
        elif event.message.text == '@本期中獎號碼':
            mtext = TextSendMessage(text= Invoice.getstr(Invoice.now))
        elif event.message.text == '@前期中獎號碼':
            mtext = TextSendMessage(text=Invoice.getstr(Invoice.before1) + '\n\n' + Invoice.getstr(Invoice.before2))
        elif event.message.text == '@對發票':
            mtext = TextSendMessage(text="請輸入發票最後三碼進行對獎！")
        elif is_threeDigit_int(event.message.text) :
            mtext = TextSendMessage(text= Invoice.On_invoices(event.message.text))
        else:
            mtext = TextSendMessage(text="你傳啥??")
    #撰寫接受到的選項對應的動作
        line_bot_api.reply_message(event.reply_token,mtext)
    except :
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='有問題喔!'))

@handler.add(MessageEvent ,message=ImageMessage)
def handle_message_image(event):
    ext = '.jpg'
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(event.message.id + ext,'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已儲存!'))

if __name__ == '__main__':
    app.run()
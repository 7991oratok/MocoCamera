# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime      
import requests                          
import time
import os
import cv2


API_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CHANNEL   = 'XXXXXXXXXXXXXXXXXXXXXXXx'
FILENAME  = "my_picture_1.jpg"
ImagePath = 'temp/my_picture_1.jpg'

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
@respond_to('moco')
@respond_to('モコ')
@respond_to('もこ')
def mention_func(message):
    message.reply('mocoの写真を送信します') # メンション


@respond_to('写真')
def takepicture_func(message):
    #写真撮影
    save_frame_camera_key(0, 'data', 'my_picture')

    #画像のアップロード
    upload_picture(API_TOKEN, CHANNEL, FILENAME, "moco 撮影", ImagePath)


# 写真撮影関数
def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    ret, frame = cap.read()
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    cv2.imwrite('{}_{}.{}'.format(base_path, 1, ext), frame)
    #cv2.destroyWindow(window_name)


#　写真アップロード関数
def upload_picture(api_token, channel, filename, message, imagepath):
    TITLE = datetime(*time.localtime(os.path.getctime(ImagePath))[:6])
    files = {'file': open(imagepath, 'rb')}
    param = {
        'token':api_token, 
        'channels':channel,
        'filename':filename,
        'initial_comment': message,'title': TITLE
    }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)



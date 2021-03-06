import os
from flask import Flask, abort, request
import pyrebase
from datetime import datetime, timedelta
from time import sleep
import urllib

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage, ImageMessage
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

app = Flask(__name__)
# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

config = {
    "apiKey": "AIzaSyALiO25iMMwqT7PJf_FqgX_7Y4L6MxQtMY",
    "authDomain": "fast-mariner-312118.firebaseapp.com",
    "databaseURL": "https://fast-mariner-312118-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "fast-mariner-312118",
    "storageBucket": "fast-mariner-312118.appspot.com",
    "messagingSenderId": "779980589461",
    "appId": "1:779980589461:web:0d466ff5620c41c6c44e9c",
    "measurementId": "G-1KZ5ZQVLYD"
}

def saveupdata():
    # 存檔的時間
    nowday = datetime.now().strftime('%Y_%m_%d')
    deltime = (datetime.now() + timedelta(seconds=-8)).strftime('%Y_%m_%d_%H_%M_%S')
    # 上傳準備
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    # 指定資料庫位置
    path_on_cloud = nowday + '/GaoJiJia_' + deltime + '.png'
    try:
        # 上傳 回存儲url
        url = storage.child(path_on_cloud).get_url(None)
        urllib.request.urlopen(url).read()
        random_img_url = storage.child(path_on_cloud).get_url(None)
        sleep(8)
        return random_img_url
    except:
        pass

# 接收 LINE 的資訊
@app.route("/", methods=["GET", "POST"])
def callback():
    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return "OK"


# 收發訊息
# 當收到 MessageEvent (信息事件)，而且信息是屬於 TextMessage (文字信息)的時候，就執行下列程式碼。
@handler.add(MessageEvent, message=TextMessage)
# 定義一個函數，該函數會接收 LINE 發送過來的資訊，並貼上event的標籤，方便後續的操作。
def handle_message(event):
    while True:
        try:
            random_img_url = 0
            saveupdata()
            line_bot_api.push_message('U1110b9cf839a201aa15f37aaf5a71ea3',
                                      ImageSendMessage(
                                          original_content_url=random_img_url,
                                          preview_image_url=random_img_url))
        except:
            pass

if __name__ == "__main__":
    app.run()

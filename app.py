# 載入需要的模組
import os
from datetime import datetime
from flask import Flask, abort, request
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
# 接收 LINE 的資訊
@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        print(body)

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
    # 排除測試數據
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        try:
            if event.message.text == "圖片":
                random_img_url, original_content_url, preview_image_url = 'https://obs.line-scdn.net/0hnNQgOqVAMWFsHieD8Z9ONk1DOgNffC9qTnh5A00WblhDL39ZVnx2UEhNZgRDfnU3VysqASceZwNJK3cxUz1_UhsePFcTKQ/f256x256'

                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=random_img_url,
                        preview_image_url=random_img_url
                    )
                )
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url, preview_image_url))      except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='沒收到訊息再發送一次'))
        
    # Send To Line
    # reply =TextSendMessage(text = fun1+'$ LINE 0x100001 $', emojis=[emoji])
    line_bot_api.reply_message(event.reply_token, reply)
if __name__ == "__main__":
    app.run()

import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    text_message = TextSendMessage(text='$ LINE emoji $')
    if get_message == "長輩在不在?":
        reply =ImageSendMessage(
        original_content_url='https://github.com/Ku-hsun/Flask-LINE-Bot-Heroku/blob/main/img/FDA9DA75-9EF4-4B95-B03C-C9F8869A2339.jpg',
        preview_image_url='https://github.com/Ku-hsun/Flask-LINE-Bot-Heroku/blob/main/img/FDA9DA75-9EF4-4B95-B03C-C9F8869A2339.jpg'
        )
    else:
        reply =ImageSendMessage(
        original_content_url='https://github.com/Ku-hsun/Flask-LINE-Bot-Heroku/blob/main/img/S__92119050.jpg',
        preview_image_url='https://github.com/Ku-hsun/Flask-LINE-Bot-Heroku/blob/main/img/S__92119050.jpg'
        )
        
    # Send To Line
    # reply =TextSendMessage(text = fun1+'$ LINE 0x100001 $', emojis=[emoji])
    line_bot_api.reply_message(event.reply_token, reply)

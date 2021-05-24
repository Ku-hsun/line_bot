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



# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        try:
            if event.source.user_id =='U1110b9cf839a201aa15f37aaf5a71ea3':
                line_bot_api.push_message('Ub90bfa0f7f6d95c8a306bc95f4f0fad4',
                                          TextSendMessage(text=event.message.text))
            elif event.source.user_id =='Ub90bfa0f7f6d95c8a306bc95f4f0fad4':
                line_bot_api.push_message('U1110b9cf839a201aa15f37aaf5a71ea3',
                                          TextSendMessage(text=event.message.text))
            else:
                line_bot_api.push_message('U1110b9cf839a201aa15f37aaf5a71ea3',
                                          TextSendMessage(text=str(event.source.user_id)))
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text))
        
    # Send To Line
    # reply =TextSendMessage(text = fun1+'$ LINE 0x100001 $', emojis=[emoji])
    line_bot_api.reply_message(event.reply_token, reply)
if __name__ == "__main__":
    app.run()

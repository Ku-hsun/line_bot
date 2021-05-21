from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('zN5Iy7Il6/sI8+F23sdopzWaWW/+PHsEGci9seuvObt0dB49EF8p7/3q3legaZ+gAqSldhMzdd2tLjeot4/9VzEJ+UghJU9Wspjx09PMRobhcPskg1jg6KhOCl6own1Ke4K4kX078ZNrIQWhUjKtZwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('13c23864d56dc3b5970a0bcc0d9da1a2')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()

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

#The following two sentences are not to be mentioned elsewhere(Channel secret & Channnel token)
line_bot_api = LineBotApi('hogehugapiyo')
handler = WebhookHandler('hogehugapiyo')

@app.route("/")
def test():
    return "OK"

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

from time import time
start = {}
users = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id   #複数人の同時使用を可能にするため
    if event.message.text == "勉強開始":
        reply_message = "計測を開始しました"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0  #合計時間
        users[userId]["start"] = time() #計測開始時刻の取得
    else:
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        
        reply_message = f"ただ今の勉強時間は{hour}時間{minute}分{second}秒です。お疲れさまでした!\n本日は合計で{users[userId]['total']}秒勉強しています"
    # else:
    #     reply_message = f"あなたは「{event.message.text}」といいました"
    
    # reply_message = "test"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()

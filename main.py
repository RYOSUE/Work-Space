import json

from linebot import LineBotApi
from linebot.models import TextSendMessage

import json
file = open('info.json','r')
info = json.load(file) #jsonファイルを読み込む
# info['CHANNEL_ACCESS_TOKEN']  #CHANNEL_ACCESS_TOKENを表示

CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
#誰に何を送るかのメソッド
def main():
    USER_ID = info['USER_ID']
    messages = TextSendMessage(text="【Wake Up Call】")
    line_bot_api.push_message(USER_ID,messages=messages)

#このファイルがメインであれば実行する
if __name__ == "__main__":
    main()

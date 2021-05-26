#coding=utf-8
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

CHANNEL_ACCESS_TOKEN = "qcqxDK5+eZUgMkFnGpAXKnXA4IbpECBO2UST11a331RnekdcKNJOVqvRVVZek9Rmtfpa0CmFuw7uYFS1h5wv80krU2GtQD6B23k7yyoljqQS10xf8xO4r1tgBzGBPyrsWIa88BKiDAubQH27tPSAsAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)


def linebot_push_message(user_id):
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text='提醒您該記帳嘍!'))
        return 'success'
    except:
        return 'error'

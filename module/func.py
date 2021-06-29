from django.conf import settings
import urllib.request, csv
import re
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    StickerSendMessage,
    LocationSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    AudioSendMessage,
    VideoSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    MessageTemplateAction,
    ButtonsTemplate,
    PostbackTemplateAction,
    URITemplateAction,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn
)
import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
baseurl = 'https://moneylinebot.herokuapp.com/static/'







def sendText(event):  # 傳送文字
    try:
        message = TextSendMessage(
            text="請輸入金額"
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))




def sendImage15(event, url):  # 傳送圖片
    try:
        message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url,
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendMulti2(event):  # 多項傳送
    try:
        message = [  # 串列
            ImageSendMessage(
                original_content_url='https://drive.google.com/uc?id=1LklZgWhaOEhCZv5fSAt8p_2Vc4vpR1wy',
                preview_image_url='https://drive.google.com/uc?id=1LklZgWhaOEhCZv5fSAt8p_2Vc4vpR1wy',
            ),
            ImageSendMessage(
                original_content_url='https://drive.google.com/uc?id=1LfPLXgrMoZEiwupEg7LBRHQsfWZiOUn1',
                preview_image_url='https://drive.google.com/uc?id=1LfPLXgrMoZEiwupEg7LBRHQsfWZiOUn1',
            ),
            ImageSendMessage(
                original_content_url='https://drive.google.com/uc?id=1LcSzAiQc3eRqt6s1-OsxbnETBo7IKpST',
                preview_image_url='https://drive.google.com/uc?id=1LcSzAiQc3eRqt6s1-OsxbnETBo7IKpST',
            )

        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))



def sendStick(event):  # 傳送貼圖
    try:
        message = StickerSendMessage(  # 貼圖兩個id需查表
            package_id='6362',
            sticker_id='11087926'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendMulti(event, r):  # 多項傳送
    try:
        message = [  # 串列
            TextSendMessage(  # 傳送文字
                text=r[:-12]
            ),
            StickerSendMessage(  # 傳送貼圖
                package_id=r[-12:-8],
                sticker_id=r[-8:]
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))





def sendQuickreply(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='請選擇記帳項目',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="飲食", text="飲食")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="娛樂", text="娛樂")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="交通", text="交通")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="學業", text="學業")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="生活用品", text="生活用品")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendQuickreply2(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='請選擇必要或不必要',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="必要", text="必要")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="不必要", text="不必要")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendQuickreply3(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='請選擇要看的圖',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="當月必要與不必要總花費占比", text="當月必要與不必要總花費占比")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="當月各項總花費占比", text="當月各項總花費占比")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="當月各項必要性總花費", text="當月各項必要性總花費")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="去年與今年當月各項必要性總花費", text="去年與今年當月各項必要性總花費")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="當月各項總花費占比與去年比較之圓餅圖", text="當月各項總花費占比與去年比較之圓餅圖")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="當月必要與不必要花費占比與去年之比較圖", text="當月必要與不必要花費占比與去年之比較圖")      # 有字數限制 大概不能超過20字
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="今年與往年同月每日平均金額比較圖", text="今年與往年同月每日平均金額比較圖")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="今年與往年同月每日平均必要金額比較圖", text="今年與往年同月每日平均必要金額比較圖")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="今年與往年同月每日平均不必要金額比較圖", text="今年與往年同月每日平均不必要金額比較圖")
                    )

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))



def sendQuickreply4(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='查詢方式 : \n1. 輸入 a年月日\n   ex : a20210625\n   可以看當日記帳資料\n2. 輸入查詢上"數量"筆花費(最多10筆)\n   ex : 查詢上三筆花費\n   可查花費\n3. 輸入查詢上"數量"筆"項目"花費紀錄\n   ex : 查詢上5筆娛樂花費\n   可查該項目花費\n4. 輸入查詢第"數量"筆花費紀錄\n   ex : 查詢第5筆花費\n   可指定查第幾筆花費',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="查詢今天花費", text="查詢今天花費")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查詢昨天花費", text="查詢昨天花費")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="這個月剩多少錢能花", text="這個月剩多少錢能花")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="消費分析", text="消費分析")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查詢上一筆花費紀錄", text="查詢上一筆花費")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查詢上5筆飲食花費紀錄", text="查詢上5筆飲食花費")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendQuickreply5(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='請選擇要修改什麼',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="修改預算", text="修改預算")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="修改支出", text="修改支出")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="修改收入", text="修改收入")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))






def sendButton(event, uid):  # 按鈕樣版
    try:
        with open('registered_data.json', 'r', encoding="utf-8") as f:
            registered_data = json.load(f)

        response = [uid, registered_data[uid]["項目"], registered_data[uid]["必要"], registered_data[uid]["金額"]]

        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                #thumbnail_image_url='https://i.imgur.com/E4cOSLw.jpg',  # 顯示的圖片
                title="記帳資料是否正確?",  # 主標題
                text=response[1]+"\n"+response[2]+"支出"+"\n"+response[3]+"元",  # 副標題
                actions=[
                    MessageTemplateAction(  # 顯示文字
                        label='正確',
                        text='正確'
                    ),
                    MessageTemplateAction(  # 顯示文字
                        label='修改資料',
                        text='記支出'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))




def sendCarousel(event):  #轉盤樣板
    try:
        with open('commondata.csv', newline='', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            a = [[i[0], i[1], i[2], i[3], i[4]] for i in rows]
        a.remove(a[0])
        i = 0
        while i < len(a):
            a[i][0] = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", a[i][0])
            if len(a[i][0]) > 35:                         #  轉盤樣板有字數限制
                a[i][0] = a[i][0][:35]
            i = i + 1
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=a[0][4],
                        title=a[0][0],
                        text=a[0][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[0][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[1][4],
                        title=a[1][0],
                        text=a[1][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[1][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[2][4],
                        title=a[2][0],
                        text=a[2][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[2][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[3][4],
                        title=a[3][0],
                        text=a[3][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[3][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[4][4],
                        title=a[4][0],
                        text=a[4][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[4][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[5][4],
                        title=a[5][0],
                        text=a[5][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[5][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[6][4],
                        title=a[6][0],
                        text=a[6][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[6][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[7][4],
                        title=a[7][0],
                        text=a[7][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[7][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[8][4],
                        title=a[8][0],
                        text=a[8][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[8][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[9][4],
                        title=a[9][0],
                        text=a[9][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[9][3]
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

from django.conf import settings
import csv
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


def sendImage(imgururl, event):  # 傳送圖片
    try:
        message = ImageSendMessage(
            original_content_url=imgururl,
            preview_image_url=imgururl
        )
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


def sendMulti(event):  # 多項傳送
    try:
        message = [  # 串列
            StickerSendMessage(  # 傳送貼圖
                package_id='8525',
                sticker_id='16581308'
            ),
            TextSendMessage(  # 傳送y文字
                text="喵"
            ),
            ImageSendMessage(  # 傳送圖片
                original_content_url="https://i.imgur.com/Ch66hFy.png",
                preview_image_url="https://i.imgur.com/Ch66hFy.png"
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendPosition(event):  # 傳送位置
    try:
        message = LocationSendMessage(
            title='成大博物館',
            address='台南市東區大學路1號',
            latitude=22.996783,  # 緯度
            longitude=120.219639  # 經度
        )
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


def sendVoice(event):  # 傳送聲音
    try:
        message = AudioSendMessage(
            original_content_url=baseurl + 'm1.mp3',  # 聲音檔置於static資料夾
            duration=20000  # 聲音長度20秒
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendVedio(event):  # 傳送影片
    try:
        message = VideoSendMessage(
            original_content_url=baseurl + 'v1.mp4',  # 影片檔置於static資料夾
            preview_image_url=baseurl + 'i1.jpg'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendButton(event):  # 按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/E4cOSLw.jpg',  # 顯示的圖片
                title='按鈕樣版示範',  # 主標題
                text='請選擇：',  # 副標題
                actions=[
                    MessageTemplateAction(  # 顯示文字計息
                        label='文字訊息',
                        text='文字訊息'
                    ),
                    URITemplateAction(  # 開啟網頁
                        label='連結網頁',
                        uri='https://www.youtube.com/watch?v=072tU1tamd0'
                    ),
                    PostbackTemplateAction(  # 執行Postback功能,觸發Postback事件
                        label='回傳訊息',  # 按鈕文字
                        # text='@購買披薩',  # 顯示文字計息
                        data='action=buy'  # Postback資料
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendConfirm(event):  # 確認樣板
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定嗎？',
                actions=[
                    MessageTemplateAction(  # 按鈕選項
                        label='是',
                        text='yes'
                    ),
                    MessageTemplateAction(
                        label='否',
                        text='no'
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
        i = 0
        while i < len(a):
            a[i][0] = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", a[i][0])
            i = i + 1
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=a[1][4],
                        title=a[1][0][:35],
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
                        title=a[2][0][:35],
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
                        title=a[3][0][:35],
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
                        title=a[4][0][:35],
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
                        title=a[5][0][:35],
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
                        title=a[6][0][:35],
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
                        title=a[7][0][:35],
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
                        title=a[8][0][:35],
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
                        title=a[9][0][:35],
                        text=a[9][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[9][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=a[10][4],
                        title=a[10][0][:35],
                        text=a[10][1]+"元",
                        actions=[
                            URITemplateAction(
                                label='商品連結',
                                uri=a[10][3]
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendImgCarousel(event):  # 圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/gtWsPu9.jpg',
                        action=MessageTemplateAction(
                            label='文字訊息',
                            text='文字1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/LRoLTlK.jpg',
                        action=PostbackTemplateAction(
                            label='回傳訊息',
                            data='action=sell&item=文字2'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendPizza(event):
    try:
        message = TextSendMessage(
            text='吉娃娃'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendYes(event):
    try:
        message = TextSendMessage(
            text='感謝\n小吉',
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendBack_buy(event, backdata):  # 處理Postback
    try:
        text1 = '感謝您\n(action 的值為 ' + backdata.get('action') + ')'
        text1 += '\n(可將處理程式寫在此處。)'
        message = TextSendMessage(  # 傳送文字
            text=text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendBack_sell(event, backdata):  # 處理Postback
    try:
        message = TextSendMessage(  # 傳送文字
            text='點選的是 ' + backdata.get('item')
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

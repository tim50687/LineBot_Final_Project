from django.conf import settings

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


def sendImage(event):  # 傳送圖片
    try:
        message = ImageSendMessage(
            original_content_url="https://i.imgur.com/itLXczv.jpeg",
            preview_image_url="https://i.imgur.com/itLXczv.jpeg"
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


def sendCarousel(event):  # 轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4zSAWJ5.jpg',
                        title='這是樣板一',
                        text='第一個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息一',
                                text='文字1'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri='https://www.youtube.com/watch?v=072tU1tamd0'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息一',
                                data='action=sell&item='
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/0jpI8le.jpg',
                        title='這是樣板二',
                        text='第二個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息二',
                                text='文字2'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri='https://www.youtube.com/watch?v=072tU1tamd0'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息二',
                                data='action=sell&item=文字2'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


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

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from module import func
from urllib.parse import parse_qsl
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
Json = 'finalproject-314617-e6520a57a6fc.json' # Json 的單引號內容請改成妳剛剛下載的那個金鑰
Url = ['https://spreadsheets.google.com/feeds']
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
Sheet = GoogleSheets.open_by_key('1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY') # 這裡請輸入妳自己的試算表代號
Sheets = Sheet.sheet1
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
registered_data = {}
with open('registered_data.json', 'w', encoding="utf-8") as f:
    json.dump(registered_data, f, ensure_ascii=False)
data = {}

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        oplist = ["飲食", "娛樂", "交通", "學業", "生活用品"]
        eslist = ["必要", "不必要"]


        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    uid = event.source.user_id
                    timer = event.timestamp
                    import time
                    time_stamp = int(str(timer)[:10])
                    struct_time = time.localtime(time_stamp)  # 轉成時間元組
                    timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 轉成字串
                    rep = event.reply_token
                    if mtext == '記帳':
                        func.sendQuickreply(event)

                    elif mtext in oplist:
                        func.sendQuickreply2(event)
                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)
                        registered_data[uid] = {"項目":[], "必要":[], "金額":[], "時間":[]}
                        registered_data[uid]["項目"] = mtext
                        with open('registered_data.json', 'w', encoding="utf-8") as f:
                            json.dump(registered_data, f, ensure_ascii=False)

                    elif mtext in eslist:
                        func.sendText(event)
                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)
                        registered_data[uid]["必要"] = mtext
                        with open('registered_data.json', 'w', encoding="utf-8") as f:
                            json.dump(registered_data, f, ensure_ascii=False)

                    elif str.isdigit(mtext) == True:
                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)
                        registered_data[uid]["金額"] = mtext
                        registered_data[uid]["時間"] = str(time)
                        with open('registered_data.json', 'w', encoding="utf-8") as f:
                            json.dump(registered_data, f, ensure_ascii=False)
                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)


                        response = [uid, registered_data[uid]["項目"], registered_data[uid]["必要"],  registered_data[uid]["金額"], timeString]
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="記帳成功"))
                    elif mtext == '圖片':
                        func.sendImage(event)

                    elif mtext == '貼圖':
                        func.sendStick(event)

                    elif mtext == '多項回覆':
                        func.sendMulti(event)

                    elif mtext == '位置':
                        func.sendPosition(event)



                    elif mtext == '聲音':
                        func.sendVoice(event)

                    elif mtext == '影片':
                        func.sendVedio(event)

                    elif mtext == '按鈕樣板':
                        func.sendButton(event)

                    elif mtext == '確認樣板':
                        func.sendConfirm(event)

                    elif mtext == '轉盤樣板':
                        func.sendCarousel(event)

                    elif mtext == '圖片轉盤':
                        func.sendImgCarousel(event)

                    elif mtext == '購買披薩':
                        func.sendPizza(event)

                    elif mtext == 'yes':
                        func.sendYes(event)


        return HttpResponse()

    else:
        return HttpResponseBadRequest()



#if isinstance(event, PostbackEvent):  # PostbackTemplateAction觸發此事件
#    backdata = dict(parse_qsl(event.postback.data))  # 取得Postback資料
#    if backdata.get('action') == 'buy':
#        func.sendBack_buy(event, backdata)
#    elif backdata.get('action') == 'sell':
#        func.sendBack_sell(event, backdata)



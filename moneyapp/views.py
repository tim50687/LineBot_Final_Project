from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from module import func, datadata, func2 ,check
from urllib.parse import parse_qsl
from googleapiclient.http import MediaFileUpload
from credent import Google
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

import csv
from selenium import webdriver
import time
import bs4
import re
import pandas as pd
import os

Json = 'finalproject-314617-e6520a57a6fc.json'    # Json 的單引號內容剛剛下載的那個金鑰
Url = ['https://spreadsheets.google.com/feeds']
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

registered_data = {}
with open('registered_data.json', 'w', encoding="utf-8") as f:
    json.dump(registered_data, f, ensure_ascii=False)
data = {}
CLIENT_SECRET_FILE = 'client_secret_676762065519-tijh4r8hulu6ajfr2u164pqo3c3l7btp.apps.googleusercontent.com.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)






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
        # CLIENT_ID = "f469621fef60ebb"
        # title = "Uploaded with PyImgur"
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
                    cost = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'
                    location = 'D:/CTPS/herokuenv'
                    if mtext == '記收入':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入:賺金額\nex:賺1000"))

                    elif mtext[0] == "賺" and str.isdigit(mtext[1:]) == True:
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            money = mtext[1:]
                            response = [uid, money, timeString]
                            Sheet = GoogleSheets.open_by_key('1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4')
                            Sheets = Sheet.sheet1
                            Sheets.append_row(response)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="紀錄成功"))

                    elif mtext == '圖':

                        a = [uid]
                        for i in a:
                            file_metadata = {
                                "name": i,
                                'mimeType': 'application/vnd.google-apps.folder'
                            }
                            fold = service.files().create(body=file_metadata, fields='id').execute()       # 雲端資料夾的id


                    elif mtext == '記支出':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            func.sendQuickreply(event)


                    elif mtext in oplist:
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            func.sendQuickreply2(event)
                            with open('registered_data.json', 'r', encoding="utf-8") as f:
                                registered_data = json.load(f)
                            registered_data[uid] = {"項目": [], "必要": [], "金額": [], "時間": []}
                            registered_data[uid]["項目"] = mtext
                            with open('registered_data.json', 'w', encoding="utf-8") as f:
                                json.dump(registered_data, f, ensure_ascii=False)


                    elif mtext in eslist:
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入金額(純數字)"))
                            with open('registered_data.json', 'r', encoding="utf-8") as f:
                                registered_data = json.load(f)
                            registered_data[uid]["必要"] = mtext
                            with open('registered_data.json', 'w', encoding="utf-8") as f:
                                json.dump(registered_data, f, ensure_ascii=False)


                    elif str.isdigit(mtext) == True:
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            with open('registered_data.json', 'r', encoding="utf-8") as f:
                                registered_data = json.load(f)
                            registered_data[uid]["金額"] = mtext
                            registered_data[uid]["時間"] = str(time)
                            with open('registered_data.json', 'w', encoding="utf-8") as f:
                                json.dump(registered_data, f, ensure_ascii=False)

                            func.sendButton(event, uid)


                    elif mtext == "正確":
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            with open('registered_data.json', 'r', encoding="utf-8") as f:
                                registered_data = json.load(f)
                            response = [uid, registered_data[uid]["項目"], registered_data[uid]["必要"],
                                        registered_data[uid]["金額"], timeString]
                            Sheet = GoogleSheets.open_by_key('19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c')
                            Sheets = Sheet.sheet1
                            Sheets.append_row(response)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="記帳成功"))


                    elif mtext == '今年與往年同月每日平均金額比較圖':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))

                        else:
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = str(int(year) - 1) + month
                            if func2.is_in_or_not_cost(uid, time) == "bad":
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="資料還不夠 記帳滿一年就可以看囉><"))
                            else:
                                datadata.current_previous_same_month_day_Line_Chart(uid, cost)
                                filename = uid + '1.png'
                                file_metadata = {
                                    'name': filename,
                                    'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                                    }
                                media = MediaFileUpload(location + '/invoicehero/{}'.format(filename), mimetype='image/png')  # 圖片在本機的位置
                                id = service.files().create(
                                    body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                    ).execute()['id']
                                url = 'https://drive.google.com/uc?id=' + id

                                func.sendImage15(event, url)









                    elif mtext == '今年與往年同月每日平均必要金額比較圖':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))

                        else:
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = str(int(year) - 1) + month
                            if func2.is_in_or_not_cost(uid, time) == "bad":
                                line_bot_api.reply_message(event.reply_token,
                                                           TextSendMessage(text="資料還不夠 記帳滿一年就可以看囉><"))
                            else:
                                datadata.current_previous_necessary_same_month_day_Line_Chart(uid, cost)
                                filename = uid + '2.png'
                                file_metadata = {
                                    'name': filename,
                                    'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                                }
                                media = MediaFileUpload(location + '/invoicehero/{}'.format(filename), mimetype='image/png')  # 圖片在本機的位置
                                id = service.files().create(
                                    body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                ).execute()['id']
                                url = 'https://drive.google.com/uc?id=' + id

                                func.sendImage15(event, url)



                    elif mtext == '今年與往年同月每日平均不必要金額比較圖':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))

                        else:
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = str(int(year) - 1) + month
                            if func2.is_in_or_not_cost(uid, time) == "bad":
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="資料還不夠 記帳滿一年就可以看囉><"))
                            else:
                                datadata.current_previous_unnecessary_same_month_day_Line_Chart(uid, cost)
                                filename = uid + '3.png'
                                file_metadata = {
                                    'name': filename,
                                    'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                                }
                                media = MediaFileUpload(location + '/invoicehero/{}'.format(filename), mimetype='image/png')  # 圖片在本機的位置
                                id = service.files().create(
                                    body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                ).execute()['id']
                                url = 'https://drive.google.com/uc?id=' + id

                                func.sendImage15(event, url)






                    elif mtext == '當月必要與不必要總花費占比':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))
                        else:
                            datadata.current_month_necessary_and_unnecessary_Pie_Chart(uid, cost)
                            filename = uid + '4.png'
                            file_metadata = {
                                'name': filename,
                                'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                            }
                            media = MediaFileUpload(location + '/invoicehero/{}'.format(filename), mimetype='image/png')  # 圖片在本機的位置
                            id = service.files().create(
                                body=file_metadata,
                                media_body=media,
                                fields='id'
                            ).execute()['id']
                            url = 'https://drive.google.com/uc?id=' + id

                            func.sendImage15(event, url)


                    elif mtext == '當月必要與不必要花費占比與去年之比較圖':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))

                        else:
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = str(int(year) - 1) + month
                            if func2.is_in_or_not_cost(uid, time) == "bad":
                                line_bot_api.reply_message(event.reply_token,
                                                           TextSendMessage(text="資料還不夠 記帳滿一年就可以看囉><"))
                            else:
                                datadata.current_month_necessary_and_unnecessary_double_Pie_Chart(uid, cost)
                                filename = uid + '5.png'
                                file_metadata = {
                                    'name': filename,
                                    'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                                }
                                media = MediaFileUpload(location + '/invoicehero/{}'.format(filename), mimetype='image/png')  # 圖片在本機的位置
                                id = service.files().create(
                                    body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                ).execute()['id']
                                url = 'https://drive.google.com/uc?id=' + id

                                func.sendImage15(event, url)




                    elif mtext == '當月各項總花費占比':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))
                        else:
                            datadata.current_month_item_Pie_Chart(uid, cost)
                            filename = uid + '6.png'
                            file_metadata = {
                                'name': filename,
                                'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                            }
                            media = MediaFileUpload(location + '/invoicehero/{}'.format(filename), mimetype='image/png')  # 圖片在本機的位置
                            id = service.files().create(
                                body=file_metadata,
                                media_body=media,
                                fields='id'
                            ).execute()['id']
                            url = 'https://drive.google.com/uc?id=' + id

                            func.sendImage15(event, url)




                    elif mtext == '當月各項總花費占比與去年比較之圓餅圖':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))

                        else:
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = str(int(year) - 1) + month
                            if func2.is_in_or_not_cost(uid, time) == "bad":
                                line_bot_api.reply_message(event.reply_token,
                                                           TextSendMessage(text="資料還不夠 記帳滿一年就可以看囉><"))
                            else:
                                datadata.current_month_item_Pie_Chart(uid, cost)
                                filename = uid + '7.png'
                                file_metadata = {
                                    'name': filename,
                                    'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                                }
                                media = MediaFileUpload(location + '/invoicehero/{}'.format(filename),
                                                        mimetype='image/png')  # 圖片在本機的位置
                                id = service.files().create(
                                    body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                ).execute()['id']
                                url = 'https://drive.google.com/uc?id=' + id

                                func.sendImage15(event, url)



                    elif mtext == '當月各項必要性總花費':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))
                        else:
                            datadata.current_month_necessary_and_unnecessary_item_Bar_Chart(uid, cost)
                            filename = uid + '8.png'
                            file_metadata = {
                                'name': filename,
                                'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                            }
                            media = MediaFileUpload(location + '/invoicehero/{}'.format(filename),
                                                    mimetype='image/png')  # 圖片在本機的位置
                            id = service.files().create(
                                body=file_metadata,
                                media_body=media,
                                fields='id'
                            ).execute()['id']
                            url = 'https://drive.google.com/uc?id=' + id

                            func.sendImage15(event, url)


                    elif mtext == '去年與今年當月各項必要性總花費':
                        if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))

                        else:
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = str(int(year) - 1) + month
                            if func2.is_in_or_not_cost(uid, time) == "bad":
                                line_bot_api.reply_message(event.reply_token,
                                                           TextSendMessage(text="資料還不夠 記帳滿一年就可以看囉><"))
                            else:
                                datadata.current_month_necessary_and_unnecessary_item_comparison_Bar_Chart(uid, cost)
                                filename = uid + '9.png'
                                file_metadata = {
                                    'name': filename,
                                    'parents': ["1C-84x5gomshiGb1wxDxemewMyLwwsU1m"]
                                }
                                media = MediaFileUpload('D:/CTPS/herokuenv/invoicehero/{}'.format(filename),
                                                        mimetype='image/png')  # 圖片在本機的位置
                                id = service.files().create(
                                    body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                ).execute()['id']
                                url = 'https://drive.google.com/uc?id=' + id

                                func.sendImage15(event, url)



                    # 上傳imgur
                    #elif mtext == '去年與今年當月各項必要性總花費':
                     #   datadata.current_month_necessary_and_unnecessary_item_comparison_Bar_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                      #  PATH9 = "send9.png"  # 圖片名稱
                       # im = pyimgur.Imgur(CLIENT_ID)
                        #uploaded_image9 = im.upload_image(PATH9, title=title)
                        #imgururl9 = uploaded_image9.link
                        #func.sendImage9(imgururl9, event)

                    elif mtext[-2:]=='花費' and len(mtext.split('花')[0]) < 5 :
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check.check_date_spend_record(uid, mtext)))


                    elif mtext[0] == 'a':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                                text=check.check_spend_data_from_date(uid, mtext[1:])))


                    elif mtext[-2:]=='花費' and len(mtext.split('花')[0]) == 5 :
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check.check_last_spend_data(uid, mtext)))


                    elif mtext[-2:]=='花費' and len(mtext.split('花')[0]) > 5 :
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                                text=check.check_last_item_spend_data(uid, mtext)))

                    elif mtext[:3]=='查詢第':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                                text=check.check_number_records_in_spend_data(uid, mtext)))




                    elif mtext == '查詢':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            func.sendQuickreply4(event)


                    elif mtext == '說明書':
                        func.sendMulti2(event)




                    elif mtext == '圖表':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            i = 1
                            b = []
                            while i < 10:
                                a = uid + str(i) + ".png"
                                filepath = location + "/invoicehero/" + a
                                if os.path.isfile(filepath):
                                    b.append("good")
                                else:
                                    b.append("bad")
                                i = i + 1
                            print(b)
                            i = 0
                            while i < 9:
                                a = uid + str(i+1) + ".png"
                                filepath = location + "/invoicehero/" + a
                                if b[i] == "good":
                                    try:
                                        os.remove(filepath)
                                    except OSError as e:
                                        print(e)
                                else:
                                    print("File is not in")
                                i = i + 1
                            func.sendQuickreply3(event)



                    elif mtext[0] == "@" and str.isdigit(mtext[1:]) == True:
                        money = mtext[1:]
                        response = [uid, money, timeString]
                        Sheet = GoogleSheets.open_by_key('14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA')
                        Sheets = Sheet.sheet1
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="紀錄成功"))




                    elif mtext == "修改資料":
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            func.sendQuickreply5(event)


                    elif mtext[:2] == "刪除":
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            Sheet = GoogleSheets.open_by_key('19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c')
                            Sheets = Sheet.sheet1
                            sp = mtext.split(" ")
                            rownumber = func2.find_row(uid, sp[0][2:], sp[1], sp[2], sp[3])
                            if rownumber == 0:
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有這筆資料 或是輸入錯誤"))
                            else:
                                Sheets.delete_row(rownumber)
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="支出刪除成功"))


                    elif mtext[:2] == "補記":
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            Sheet = GoogleSheets.open_by_key('19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c')
                            Sheets = Sheet.sheet1
                            sp = mtext.split(" ")
                            row = [uid, sp[0][2:], sp[1], sp[2], sp[3][:4] + "-" + sp[3][4:6] + "-" + sp[3][6:9]]
                            Sheets.append_row(row)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="支出補記成功"))


                    elif mtext[:2] == "刪掉":
                        if func2.is_in_or_not(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token,
                                                       TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            Sheet = GoogleSheets.open_by_key('1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4')
                            Sheets = Sheet.sheet1
                            income = mtext[2:]
                            string = func2.get_today_date()
                            year = string[:4]  # 年
                            month = string[4:6]  # 月
                            time = year + month
                            rownumber = func2.find_row_income(uid, income, time)
                            if rownumber == 0:
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有這筆資料 或是輸入錯誤"))
                            else:
                                Sheets.delete_row(rownumber)
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="收入刪除成功"))

                    elif mtext == "修改收入":
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="輸入方式:刪掉金額(數字)\nex:刪掉500"))

                    elif mtext == "修改預算":
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="輸入方式:改成金額(數字)\nex:改成5000"))

                    elif mtext == "修改支出":
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="輸入:刪除(或補記)項目 必要性 金額 年月日\nex : 刪除飲食 不必要 20 20210605"))

                    elif mtext[:2] == "改成":
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            index = func2.find_row_money(uid, func2.get_today_date()[:6])
                            Sheet = GoogleSheets.open_by_key('14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA')
                            Sheets = Sheet.sheet1
                            sp = mtext[2:]
                            if index == 0:
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有這筆資料 或是輸入錯誤"))
                            else:
                                index = "B" + str(index)
                                Sheets.update(index, sp)
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="預算修改成功"))


                    elif mtext == '這個月剩多少錢能花':
                        if func2.is_in_or_not(uid , func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            r = func2.average(uid, func2.get_today_date()[:6])
                            func.sendMulti(event, r)




                    elif mtext == '比價':
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入:XX多少錢\nex:iPhone 12多少錢\n大約要等20秒~"))

                    elif mtext[-3:] == '多少錢':
                        product = mtext[:-3]
                        pd.set_option('display.unicode.ambiguous_as_wide', True)
                        pd.set_option('display.unicode.east_asian_width', True)
                        pd.set_option('display.max_columns', 10)
                        pd.set_option('display.max_colwidth', 200)
                        pd.set_option('display.width', None)

                        driver = webdriver.Chrome(location + '/invoicehero/chromedriver.exe')
                        url = 'https://feebee.com.tw/'

                        def url_pagesource(text):
                            driver.get(url)
                            # To find the ID and search the content
                            driver.find_element_by_id('search').send_keys(str(text + "\n"))
                            # currentURL = driver.current_url #decode 過了?

                            # get page source
                            PageSource = driver.page_source

                            ## 用 bs4 抓資料
                            soup = bs4.BeautifulSoup(PageSource, "html.parser")
                            return soup

                        def nextPage(pageURL):
                            driver.get(url)
                            PageSource = driver.page_source
                            soup = bs4.BeautifulSoup(PageSource, "html.parser")
                            ######## 價格有範圍的(抓最好的)
                            ##get the link
                            http0 = []
                            https0 = soup.select("div.product_group_store ol")
                            for link in https0:
                                http0.append(link.a.get("href"))
                            ## get the img
                            img0 = []
                            imgs0 = soup.select("li.product_group span.img_container a.product_link img")
                            for pic in imgs0:
                                img0.append(pic.get("data-src"))
                            ## get the shop
                            range_shops = soup.select("div.product_group_store ol")
                            shops0 = []
                            for shop in range_shops:
                                xx = shop.span.get_text()
                                shops0.append(xx)
                            ## get the price
                            range_prices = soup.select("div.product_group_store ol")
                            prices0 = []
                            for money in range_prices:
                                yy = money.a.get_text()
                                if "PChome" in yy:
                                    yy = re.sub(r"PChome24h購物", "", yy)
                                    yy = re.sub(r"\n|[\u4e00-\u9fa5]|[A-Za-z]", "", yy)
                                else:
                                    yy = re.sub(r"\n|[\u4e00-\u9fa5]|[A-Za-z]", "", yy)
                                prices0.append(yy)
                            ## get the title
                            range_titles = soup.select("div.product_group__content h3.product__title")
                            titles0 = []
                            for title in range_titles:
                                zz = title.get_text()
                                titles0.append(zz)

                            ######## 推薦商品
                            ##get the link
                            http1 = []
                            https1 = soup.select("li.campaign span.items_container > a.campaign_link_title")
                            for link in https1:
                                http1.append(link.get("href"))
                            ## get the img
                            img1 = []
                            imgs1 = soup.select("li.campaign span.img_container a.campaign_link img")
                            for pic in imgs1:
                                img1.append(pic.get("data-src"))
                            ## get the title
                            titles1 = []
                            Prefertitles = soup.select("a.campaign_link h3.large")
                            for prefertitle in Prefertitles:
                                titles1.append(prefertitle.get_text())
                            ## get the shop
                            shops1 = []
                            PreferShops = soup.select("div.ellipsis div.promote_info span.shop")
                            for prefershop in PreferShops:
                                Nospace = prefershop.get_text().replace(" ", "").replace("\n", "")
                                shops1.append(Nospace)
                            ## get the price
                            prices1 = []
                            Preferprices = soup.select("a.campaign_link span.price")
                            for preferprice in Preferprices:
                                prices1.append(preferprice.get_text())
                            nextlink = soup.find("a", class_="page_next")
                            return http0, img0, titles0, prices0, shops0, \
                                   http1, img1, titles1, prices1, shops1, \
                                   nextlink.get('href')

                        def crawl(pagesource):
                            ######## 價格有範圍的(抓最好的)
                            ##get the link
                            http0 = []
                            https0 = pagesource.select("div.product_group_store ol")
                            for link in https0:
                                http0.append(link.a.get("href"))
                            ## get the img
                            img0 = []
                            imgs0 = pagesource.select("li.product_group span.img_container a.product_link img")
                            for pic in imgs0:
                                img0.append(pic.get("data-src"))
                            ## get the shop
                            range_shops = pagesource.select("div.product_group_store ol")
                            shops0 = []
                            for shop in range_shops:
                                xx = shop.span.get_text()
                                shops0.append(xx)
                            ## get the price
                            range_prices = pagesource.select("div.product_group_store ol")
                            prices0 = []
                            for money in range_prices:
                                yy = money.a.get_text()
                                if "PChome" in yy:
                                    yy = re.sub(r"PChome24h購物", "", yy)
                                    yy = re.sub(r"\n|[\u4e00-\u9fa5]|[A-Za-z]", "", yy)
                                else:
                                    yy = re.sub(r"\n|[\u4e00-\u9fa5]|[A-Za-z]", "", yy)
                                prices0.append(yy)
                            ## get the title
                            range_titles = pagesource.select("div.product_group__content h3.product__title")
                            titles0 = []
                            for title in range_titles:
                                zz = title.get_text()
                                titles0.append(zz)

                            ######## 推薦商品
                            ##get the link
                            http1 = []
                            https1 = pagesource.select("li.campaign span.items_container > a.campaign_link_title")
                            for link in https1:
                                http1.append(link.get("href"))
                            ## get the img
                            img1 = []
                            imgs1 = pagesource.select("li.campaign span.img_container a.campaign_link img")
                            for pic in imgs1:
                                img1.append(pic.get("data-src"))
                            ## get the title
                            titles1 = []
                            Prefertitles = pagesource.select("a.campaign_link h3.large")
                            for prefertitle in Prefertitles:
                                titles1.append(prefertitle.get_text())
                            ## get the shop
                            shops1 = []
                            PreferShops = pagesource.select("div.ellipsis div.promote_info span.shop")
                            for prefershop in PreferShops:
                                Nospace = prefershop.get_text().replace(" ", "").replace("\n", "")
                                shops1.append(Nospace)
                            ## get the price
                            prices1 = []
                            Preferprices = pagesource.select("a.campaign_link span.price")
                            for preferprice in Preferprices:
                                prices1.append(preferprice.get_text())

                            nextlink = pagesource.find("a", class_="page_next")
                            if nextlink != None:
                                return http0, img0, titles0, prices0, shops0, \
                                        http1, img1, titles1, prices1, shops1, \
                                        nextlink.get('href')
                            elif nextlink == None:
                                return http0, img0, titles0, prices0, shops0, \
                                        http1, img1, titles1, prices1, shops1


                        result = crawl(url_pagesource(product))
                        if len(result) == 10:
                            http0, img0, titles0, prices0, shops0, http1, img1, titles1, prices1, shops1 = result
                        else:
                            http0, img0, titles0, prices0, shops0, http1, img1, titles1, prices1, shops1, next = result
                            url = 'https://feebee.com.tw' + next
                            Nextresult = nextPage(url)
                            Shttp0, Simg0, Stitles0, Sprices0, Sshops0, Shttp1, Simg1, Stitles1, Sprices1, Sshops1, Snext = Nextresult
                            http0.extend(Shttp0)
                            http1.extend(Shttp1)
                            img0.extend(Simg0)
                            img1.extend(Simg1)
                            titles0.extend(Stitles0)
                            titles1.extend(Stitles1)
                            prices0.extend(Sprices0)
                            prices1.extend(Sprices1)
                            shops0.extend(Sshops0)
                            shops1.extend(Sshops1)

                        #
                        # Pandas
                        rangeData = pd.DataFrame({
                            "商品": titles0,
                            "商品價格": prices0,
                            "販售商城": shops0,
                            "商品網址": http0,
                            "圖片網址": img0
                        })
                        Preferdata = pd.DataFrame({
                            "商品": titles1,
                            "商品價格": prices1,
                            "販售商城": shops1,
                            "商品網址": http1,
                            "圖片網址": img1
                        })

                        a = pd.concat([rangeData, Preferdata], keys=["篩選過", "推薦"])
                        #print(a)
                        a.to_csv("commondata.csv", index=False, encoding=("utf-8-sig"))  ## utf-8-sig 解決亂碼問題


                        func.sendCarousel(event)










                    elif mtext == '消費分析':
                        if func2.is_in_or_not(uid, func2.get_today_date()[:6]) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            if func2.is_in_or_not_cost(uid, func2.get_today_date()[:6]) == "bad":
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您還沒有紀錄支出呦"))
                            else:
                                string = func2.get_today_date()
                                year = string[:4]  # 年
                                month = string[4:6]  # 月
                                eatcost = func2.item_cost(uid, "飲食", year + month)
                                playcost = func2.item_cost(uid, "娛樂", year + month)
                                trafcost = func2.item_cost(uid, "交通", year + month)
                                thingcost = func2.item_cost(uid, "生活用品", year + month)
                                monthcost = func2.month_cost(uid, year + month)
                                ratio = round(eatcost / monthcost)
                                ratio2 = round(playcost / monthcost)
                                ratio3 = round(trafcost / monthcost)
                                ratio4 = round(thingcost / monthcost)

                                if ratio < 0.38:
                                    reply1 = "您在「飲食」的花費「低於」一般大學生"
                                else:
                                    reply1 = "您在「飲食」的花費「高於」一般大學生"
                                if ratio2 < 0.13:
                                    reply2 = "您在「娛樂」的花費「低於」一般大學生"
                                else:
                                    reply2 = "您在「娛樂」的花費「高於」一般大學生"
                                if ratio3 < 0.15:
                                    reply3 = "您在「交通」的花費「低於」一般大學生"
                                else:
                                    reply3 = "您在「交通」的花費「高於」一般大學生"
                                if ratio4 < 0.2:
                                    reply4 = "您在「生活」的花費「低於」一般大學生"
                                else:
                                    reply4 = "您在「生活」的花費「高於」一般大學生"

                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply1 + "\n" + reply2 + "\n" + reply3 + "\n" + reply4))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="格式錯誤"))



        return HttpResponse()

    else:
        return HttpResponseBadRequest()

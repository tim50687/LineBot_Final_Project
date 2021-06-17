from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from module import func, datadata, func2 ,check
from urllib.parse import parse_qsl
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

import csv
from selenium import webdriver
import time
import bs4
import re
import pandas as pd
import pyimgur
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
        CLIENT_ID = "f469621fef60ebb"
        title = "Uploaded with PyImgur"
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

                    if mtext == '記收入':
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入:/金額\nex:/1000"))

                    elif mtext[0] == "/":
                        money = mtext[1:]
                        response = [uid, money, timeString]
                        Sheet = GoogleSheets.open_by_key('1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4')
                        Sheets = Sheet.sheet1
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="紀錄成功"))

                    elif mtext == '記支出':
                        if func2.is_in_or_not(uid) == "bad":
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先登錄每月預算\n登錄方式:@金額\nex:@8000"))
                        else:
                            func.sendQuickreply(event)


                    elif mtext in oplist:
                        func.sendQuickreply2(event)
                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)
                        registered_data[uid] = {"項目": [], "必要": [], "金額": [], "時間": []}
                        registered_data[uid]["項目"] = mtext
                        with open('registered_data.json', 'w', encoding="utf-8") as f:
                            json.dump(registered_data, f, ensure_ascii=False)

                    elif mtext in eslist:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入金額(純數字)"))
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

                        func.sendButton(event, uid)

                    elif mtext == "正確":

                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)
                        response = [uid, registered_data[uid]["項目"], registered_data[uid]["必要"],  registered_data[uid]["金額"], timeString]
                        Sheet = GoogleSheets.open_by_key('19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c')
                        Sheets = Sheet.sheet1
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="記帳成功"))

                    elif mtext == '今年與往年同月每日平均金額比較圖':
                        datadata.current_previous_same_month_day_Line_Chart('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH1 = "send1.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image1 = im.upload_image(PATH1, title=title)
                        imgururl1 = uploaded_image1.link
                        func.sendImage1(imgururl1, event)

                    elif mtext == '今年與往年同月每日平均必要金額比較圖':
                        datadata.current_previous_necessary_same_month_day_Line_Chart('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH2 = "send2.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image2 = im.upload_image(PATH2, title=title)
                        imgururl2 = uploaded_image2.link
                        func.sendImage2(imgururl2, event)

                    elif mtext == '今年與往年同月每日平均不必要金額比較圖':
                        datadata.current_previous_unnecessary_same_month_day_Line_Chart('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH3 = "send3.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image3 = im.upload_image(PATH3, title=title)
                        imgururl3 = uploaded_image3.link
                        func.sendImage3(imgururl3, event)

                    elif mtext == '當月必要與不必要總花費占比':
                        datadata.current_month_necessary_and_unnecessary_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH4 = "send4.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image4 = im.upload_image(PATH4, title=title)
                        imgururl4 = uploaded_image4.link
                        func.sendImage4(imgururl4, event)

                    elif mtext == '今年當月必要與不必要總花費占比':
                        datadata.current_month_necessary_and_unnecessary_double_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH5 = "send5.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image5 = im.upload_image(PATH5, title=title)
                        imgururl5 = uploaded_image5.link
                        func.sendImage5(imgururl5, event)
                    elif mtext == '當月各項總花費占比':
                        datadata.current_month_item_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH6 = "send6.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image6 = im.upload_image(PATH6, title=title)
                        imgururl6 = uploaded_image6.link
                        func.sendImage6(imgururl6, event)
                    elif mtext == '今年當月各項總花費占比':
                        datadata.current_month_item_double_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH7 = "send7.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image7 = im.upload_image(PATH7, title=title)
                        imgururl7 = uploaded_image7.link
                        func.sendImage7(imgururl7, event)

                    elif mtext == '當月各項必要性總花費':
                        datadata.current_month_necessary_and_unnecessary_item_Bar_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH8 = "send8.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image8 = im.upload_image(PATH8, title=title)
                        imgururl8 = uploaded_image8.link
                        func.sendImage8(imgururl8, event)

                    elif mtext == '去年與今年當月各項必要性總花費':
                        datadata.current_month_necessary_and_unnecessary_item_comparison_Bar_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH9 = "send9.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image9 = im.upload_image(PATH9, title=title)
                        imgururl9 = uploaded_image9.link
                        func.sendImage9(imgururl9, event)


                    elif mtext == '去年與今年當月各項必要性總花費':
                        datadata.current_month_necessary_and_unnecessary_item_comparison_Bar_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
                        PATH9 = "send9.png"  # 圖片名稱
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image9 = im.upload_image(PATH9, title=title)
                        imgururl9 = uploaded_image9.link
                        func.sendImage9(imgururl9, event)

                    elif mtext[-2:]=='花費' and len(mtext.split('花')[0]) < 5:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check.check_date_spend_record(uid, mtext)))

                    elif mtext[0] == 'a':
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check.check_spend_data_from_date(uid, mtext[1:])))

                    elif mtext[-2:]=='花費' and len(mtext.split('花')[0]) == 5:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=check.check_last_spend_data(uid, mtext)))

                    elif mtext[-2:]=='花費' and len(mtext.split('花')[0]) > 5:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=check.check_last_item_spend_data(uid, mtext)))


                    elif mtext == '查詢':
                        func.sendQuickreply4(event)

                    elif mtext == '圖表':
                        func.sendQuickreply3(event)



                    elif mtext[0] == "@":
                        money = mtext[1:]
                        response = [uid, money, timeString]
                        Sheet = GoogleSheets.open_by_key('14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA')
                        Sheets = Sheet.sheet1
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="紀錄成功"))


                    elif mtext == "修改資料":
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="輸入:刪除(或補記)項目 必要性 金額 年月日\nex : 刪除飲食 不必要 20 20210605"))

                    elif mtext[:2] == "刪除":
                        Sheet = GoogleSheets.open_by_key('19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c')
                        Sheets = Sheet.sheet1
                        sp = mtext.split(" ")
                        rownumber = func2.find_row(uid, sp[0][2:], sp[1], sp[2], sp[3])
                        if rownumber == 0:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有這筆資料 或是輸入錯誤"))
                        else:
                            Sheets.delete_row(rownumber)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="刪除成功"))

                    elif mtext[:2] == "補記":
                        Sheet = GoogleSheets.open_by_key('19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c')
                        Sheets = Sheet.sheet1
                        sp = mtext.split(" ")
                        row = [uid , sp[0][2:], sp[1], sp[2], sp[3][:4]+"-"+sp[3][4:6]+"-"+sp[3][6:9]]
                        Sheets.append_row(row)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="補記成功"))

                    elif mtext == '這個月剩多少錢能花':
                        r = func2.average(uid, func2.get_today_date()[:6])
                        func.sendMulti(event, r)

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

                    elif mtext == '比價':
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入:XX多少錢\nex:iPhone 12多少錢"))

                    elif mtext[-3:] == '多少錢' :
                        product = mtext[:-3]
                        pd.set_option('display.unicode.ambiguous_as_wide', True)
                        pd.set_option('display.unicode.east_asian_width', True)
                        pd.set_option('display.max_columns', 10)
                        pd.set_option('display.max_colwidth', 200)
                        pd.set_option('display.width', None)
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                        chrome_options.add_argument("--headless")
                        chrome_options.add_argument("--disable-dev-shm-usage")
                        chrome_options.add_argument("--no-sandbox")
                        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                                  chrome_options=chrome_options)
                        url = 'https://feebee.com.tw/'
                        #driver = webdriver.Chrome('D:/Download/chromedriver_win32 (1)/chromedriver.exe')
                        #driver = webdriver.Chrome('chromedriver.exe')
                        driver.get(url)

                        def url_pagesource(text):
                            # To find the ID and search the content
                            driver.find_element_by_id('search').send_keys(str(text + "\n"))
                            # currentURL = driver.current_url #decode 過了?

                            # get page source
                            PageSource = driver.page_source

                            ## 用 bs4 抓資料
                            soup = bs4.BeautifulSoup(PageSource, "html.parser")
                            return soup

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

                            ####### 一般
                            ##get the link
                            http2 = []
                            https2 = pagesource.select("li.items span.items_container > a.items_link")
                            for link in https2:
                                http2.append(link.get("href"))
                            ## get the img
                            img2 = []
                            imgs2 = pagesource.select("li.pure-g span.img_container a.items_link img")
                            for pic in imgs2:
                                img2.append(pic.get("data-src"))
                            ## get the title
                            ElementTitles = pagesource.select("a.items_link h3.large")
                            titles2 = []
                            for title in ElementTitles:
                                titles2.append(title.get_text())
                            ## get the shop
                            ElementShops = pagesource.select("span.items_container ul li.pure-g span.shop")
                            shops2 = []
                            for shop in ElementShops:
                                Nospace = shop.get_text().replace(" ", "").replace("\n", "")
                                shops2.append(Nospace)
                            ## get the price
                            ElementPrices = pagesource.select("span.items_container li.price-info span.ellipsis")
                            prices2 = []
                            for price in ElementPrices:
                                prices2.append(price.get_text())

                            ######## 繼續瀏覽
                            ##get the link
                            http3 = []
                            https3 = pagesource.select("li.bid span.bid_container")
                            for link in https3:
                                http3.append(link.a.get("href"))
                            ## get the img
                            img3 = []
                            imgs3 = pagesource.select("li.bid span.img_container a.bid_link img")
                            for pic in imgs3:
                                img3.append(pic.get("data-src"))
                            ## get the title
                            ElementTitles = pagesource.select("li.bid a.bid_link h3.large")
                            titles3 = []
                            for title in ElementTitles:
                                titles3.append(title.get_text())
                            ElementShops = pagesource.select("span.bid_container ul li.pure-g span.shop")
                            ## get the shop
                            shops3 = []
                            for shop in ElementShops:
                                Nospace = shop.get_text().replace(" ", "").replace("\n", "")
                                shops3.append(Nospace)
                            ## get the price
                            ElementPrices = pagesource.select("span.bid_container li.price-info span.ellipsis")
                            prices3 = []
                            for price in ElementPrices:
                                prices3.append(price.get_text())

                            return http0, img0, titles0, prices0, shops0, \
                                   http1, img1, titles1, prices1, shops1, \
                                   http2, img2, titles2, prices2, shops2, \
                                   http3, img3, titles3, prices3, shops3

                        ## :D
                        data = crawl(url_pagesource(product))
                        http0, img0, titles0, prices0, shops0, http1, img1, titles1, prices1, shops1, http2, img2, titles2, prices2, shops2, http3, img3, titles3, prices3, shops3 = data
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

                        Commondata = pd.DataFrame({
                            "商品": titles2,
                            "商品價格": prices2,
                            "販售商城": shops2,
                            "商品網址": http2,
                            "圖片網址": img2
                        })

                        Continue = pd.DataFrame({
                            "商品": titles3,
                            "商品價格": prices3,
                            "販售商城": shops3,
                            "商品網址": http3,
                            "圖片網址": img3
                        })

                        #
                        # #
                        # # # #
                        #a = pd.concat([rangeData, Preferdata, Commondata, Continue], keys=["篩選過", "推薦", "一般", "繼續瀏覽"])
                        #print(a)
                        #a.to_csv("commondata.csv", index=False, encoding=("utf-8-sig"))  ## utf-8-sig 解決亂碼問題

                        Sheet = GoogleSheets.open_by_key('154DRXdwIK5QhggsevsNdrL3KK3IX3pc1YwSryMQZ18A')
                        Sheets = Sheet.sheet1
                        Sheets.clear()
                        c = ["商品", "商品價格", "販售商城", "商品網址", "圖片網址"]
                        d = rangeData.values.tolist()
                        e = Preferdata.values.tolist()
                        f = Commondata.values.tolist()
                        g = Continue.values.tolist()
                        Sheets.insert_row(c, 1)
                        Sheets.append_rows(d)
                        Sheets.append_rows(e)
                        Sheets.append_rows(f)
                        Sheets.append_rows(g)
                        func.sendCarousel(event)

                    elif mtext == '消費分析':
                        string = func2.get_today_date()
                        year = string[:4]  # 年
                        month = string[4:6]  # 月
                        eatcost = func2.item_cost(uid, "飲食", year+month)
                        playcost = func2.item_cost(uid, "娛樂", year + month)
                        trafcost = func2.item_cost(uid, "交通", year + month)
                        thingcost = func2.item_cost(uid, "生活用品", year + month)
                        monthcost = func2.month_cost(uid, year+month)
                        ratio = round(eatcost/monthcost)
                        ratio2 = round(playcost/monthcost)
                        ratio3 = round(trafcost / monthcost)
                        ratio4 = round(thingcost / monthcost)
                        reply1 = ""
                        reply2 = ""
                        reply3 = ""
                        reply4 = ""
                        if ratio < 0.38:
                            reply1 = "您在「飲食」的花費「低於」一般大學生"
                        else :
                            reply1 = "您在「飲食」的花費「高於」一般大學生"
                        if ratio2 < 0.13:
                            reply2= "您在「娛樂」的花費「低於」一般大學生"
                        else :
                            reply2 = "您在「娛樂」的花費「高於」一般大學生"
                        if ratio3 < 0.15:
                            reply3= "您在「交通」的花費「低於」一般大學生"
                        else :
                            reply3 = "您在「交通」方面的花費「高於」一般大學生"
                        if ratio4 < 0.2:
                            reply4 = "您在「生活用品」的花費「低於」一般大學生"
                        else :
                            reply4 = "您在「生活用品」的花費「高於」一般大學生"

                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply1+"\n"+reply2+"\n"+reply3+"\n"+reply4))


                    elif mtext == '購買披薩':
                        func.sendPizza(event)

                    elif mtext == 'yes':
                        func.sendYes(event)

        return HttpResponse()

    else:
        return HttpResponseBadRequest()

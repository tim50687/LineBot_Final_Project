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
import csv
from selenium import webdriver
import time
import bs4
import re
import pandas as pd
import pyimgur
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
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入:我有XX元\nex:我有6000元"))

                    elif mtext[:2] == "我有" and mtext[-1] == "元":
                        money = mtext[mtext.find("有")+1:mtext.find("元")]
                        response = [uid, money, timeString]
                        Sheet = GoogleSheets.open_by_key('1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4')
                        Sheets = Sheet.sheet1
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="紀錄成功"))

                    elif mtext == '記支出':
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
                        with open('registered_data.json', 'r', encoding="utf-8") as f:
                            registered_data = json.load(f)
                        response = [uid, registered_data[uid]["項目"], registered_data[uid]["必要"],  registered_data[uid]["金額"], timeString]
                        Sheet = GoogleSheets.open_by_key('1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY')
                        Sheets = Sheet.sheet1
                        Sheets.append_row(response)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="記帳成功"))
                    elif mtext == '圖片':
                        func.sendImage(event)

                    elif mtext == '圖表':
                        CLIENT_ID = "f469621fef60ebb"
                        PATH = "rplot.jpeg"  # 圖片名稱
                        title = "Uploaded with PyImgur"
                        im = pyimgur.Imgur(CLIENT_ID)
                        uploaded_image = im.upload_image(PATH, title=title)
                        imgururl = uploaded_image.link
                        func.sendImage(imgururl, event)

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

                    elif mtext == '比價':
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入:XX多少錢\nex:iPhone 12多少錢"))

                    elif mtext[-3:] == '多少錢' :
                        product = mtext[:-3]
                        pd.set_option('display.unicode.ambiguous_as_wide', True)
                        pd.set_option('display.unicode.east_asian_width', True)
                        pd.set_option('display.max_columns', 10)
                        pd.set_option('display.max_colwidth', 200)
                        pd.set_option('display.width', None)

                        url = 'https://feebee.com.tw/'
                        #driver = webdriver.Chrome('D:/Download/chromedriver_win32 (1)/chromedriver.exe')
                        driver = webdriver.Chrome('chromedriver.exe')
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
                        a = pd.concat([rangeData, Preferdata, Commondata, Continue], keys=["篩選過", "推薦", "一般", "繼續瀏覽"])
                        print(a)
                        a.to_csv("commondata.csv", index=False, encoding=("utf-8-sig"))  ## utf-8-sig 解決亂碼問題
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

import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
Json = 'finalproject-314617-e6520a57a6fc.json' # Json 的單引號內容請改成妳剛剛下載的那個金鑰
Url = ['https://spreadsheets.google.com/feeds']
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
Sheet = GoogleSheets.open_by_key('1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY') # 這裡請輸入妳自己的試算表代號
Sheets = Sheet.sheet1
with open('data.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

a = []
for key in data.keys():
    a.append(int(key[:10]))

i = 0
c = []
while i < len(a):
    struct_time = time.localtime(a[i])  # 轉成時間元組
    timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 轉成字串
    c.append([timeString,])
    i = i + 1

b = []
for value in data.values():
    b.append(value)
i = 0
while i < len(b):
    b[i] = b[i].split("/")
    i = i + 1

datalist = ["userid", "項目", "必要嗎", "金額", "時間"]
itemlist = []
i = 0
while i < len(b):
    itemlist.append(b[i]+c[i])
    i = i + 1
dataTitle = ["userid", "項目", "必要嗎", "金額", "時間"]
i = 0
while i < len(itemlist):
    datas = itemlist[i]
    Sheets.append_row(datas)
    i = i + 1

import urllib.request, csv
url = 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'      # 下載連結
webpage = urllib.request.urlopen(url)  # 開啟網頁
data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]]for i in data]
print(a)
import urllib.request, csv


url = 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'      # 下載連結
webpage = urllib.request.urlopen(url)  # 開啟網頁
data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]]for i in data]


# 輸入userid得到他的總花費


def total_cost(userid):
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
# print(total_cost("U0a84d6de855ff90af62127932c7fde1f"))


# 輸入userid和項目得到他的該項總花費
def item_cost(userid, types):
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][1] == types:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
# print(item_cost("U0a84d6de855ff90af62127932c7fde1f", "學業"))


# 輸入userid和必要嗎得到他的該項總花費
def ess_cost(userid, types):
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][2] == types:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
# print(ess_cost("U0a84d6de855ff90af62127932c7fde1f", "必要"))


# 輸入userid和日期得到他的該天總花費
def day_cost(userid, types):
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][4][5:7]+a[i][4][8:10] == types:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
# print(day_cost("U0a84d6de855ff90af62127932c7fde1f", "0524"))








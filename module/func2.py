import urllib.request, csv
import time as t
import datetime
url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'      # 下載連結
webpage = urllib.request.urlopen(url)  # 開啟網頁
data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]]for i in data]
# 輸入userid得到他的總花費
#print(a)

def total_cost(userid):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
# print(total_cost("U0a84d6de855ff90af62127932c7fde1f"))


# 輸入userid和項目和年月得到他的該項總花費
def item_cost(userid, types, time):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][1] == types and a[i][4][:4]+a[i][4][5:7] == time:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
#print(item_cost("U0a84d6de855ff90af62127932c7fde1f", "學業", "202106"))


# 輸入userid和必要嗎得到他的該項總花費
def ess_cost(userid, types):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][2] == types:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
# print(ess_cost("U0a84d6de855ff90af62127932c7fde1f", "必要"))


# 輸入userid和年月得到他的該月總花費
def month_cost(userid, types):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][4][:4]+a[i][4][5:7] == types:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)
#print(month_cost("U0a84d6de855ff90af62127932c7fde1f", "202106"))

# 輸入userid和日期得到他的該天總花費
def day_cost(userid, types):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and a[i][4][5:7]+a[i][4][8:10] == types:
            b.append(int(a[i][3]))
        i = i + 1
    return sum(b)


# 輸入userid和日期得到他的該天花費明細
def day_cost_list(userid, types):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    while i < len(a):
        if a[i][0] == userid and  a[i][4][:4]+a[i][4][5:7]+a[i][4][8:10] == types:
            b.append(a[i][1]+" "+a[i][2]+"支出"+" "+a[i][3]+"元")
        i = i + 1
    return "\n-------------------\n".join(b)

#print(day_cost_list("U0a84d6de855ff90af62127932c7fde1f", "20210615"))


# 輸入年月日 項目 必要性支出 金額 刪除資料

def find_row(userid, item, ess, digit, time):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    i = 0
    b = []
    reply = -2
    while i < len(a):
        if userid == a[i][0] and item == a[i][1] and digit == a[i][3] and ess == a[i][2] and time == a[i][4][:4]+a[i][4][5:7]+a[i][4][8:10]:
            b.append(str(i))
            if len(b) > 0:
                reply = b[0]
        i = i + 1
    return int(reply) + 2
# print(delete_by_row("U0a84d6de855ff90af62127932c7fde1f", "飲食", "不必要", "98", "20210602"))



url2 = 'https://docs.google.com/spreadsheets/d/14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA/export?format=csv'  # 下載連結
webpage = urllib.request.urlopen(url2)  # 開啟網頁
data2 = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
apple = [[i["userid"], i["金額"], i["時間"]] for i in data2]

url3 = 'https://docs.google.com/spreadsheets/d/1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4/export?format=csv'  # 下載連結
webpage = urllib.request.urlopen(url3)  # 開啟網頁
data3 = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
banana = [[i["userid"], i["金額"], i["時間"]] for i in data3]
#print(banana)



def is_in_or_not(userid, types):
    url2 = 'https://docs.google.com/spreadsheets/d/14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url2)  # 開啟網頁
    data2 = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    apple = [[i["userid"], i["金額"], i["時間"]] for i in data2]
    reply = "bad"
    i = 0
    while i < len(apple):
        if userid in apple[i] and apple[i][2][:4]+apple[i][2][5:7] == types:
            reply = "good"
        i = i + 1
    return reply


def is_in_or_not_cost(userid, types):
    url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url)  # 開啟網頁
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    a = [[i["userid"], i["項目"], i["必要嗎"], i["金額"], i["時間"]] for i in data]
    reply = "bad"
    i = 0
    while i < len(a):
        if userid in a[i] and a[i][4][:4]+a[i][4][5:7] == types:
            reply = "good"
        i = i + 1
    return reply

#print(is_in_or_not_cost('U0a84d6de855ff90af62127932c7fde1f', '202106'))


# 輸入userid和月分(202106)得到他的該月總收入
def month_income(userid, types):
    url3 = 'https://docs.google.com/spreadsheets/d/1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url3)  # 開啟網頁
    data3 = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    banana = [[i["userid"], i["金額"], i["時間"]] for i in data3]
    i = 0
    b = []
    while i < len(banana):
        if banana[i][0] == userid and banana[i][2][:4]+banana[i][2][5:7] == types:
            b.append(int(banana[i][1]))
        i = i + 1
    return sum(b)

#print(month_income('U0a84d6de855ff90af62127932c7fde1f', '05'))

# 輸入userid和月分(202106)得到他的該月總預算
def month_money(userid, types):
    url2 = 'https://docs.google.com/spreadsheets/d/14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url2)  # 開啟網頁
    data2 = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    apple = [[i["userid"], i["金額"], i["時間"]] for i in data2]
    i = 0
    b = []
    while i < len(apple):
        if apple[i][0] == userid and apple[i][2][:4]+apple[i][2][5:7] == types:
            b.append(int(apple[i][1]))
        i = i + 1
    return sum(b)

# 輸入userid和月份(202106)得到當月剩餘金額
def income_minus_cost(userid, types):
    income = month_income(userid, types)
    money = month_money(userid, types)
    cost = month_cost(userid, types)
    reply = income + money - cost
    return reply

#print(income_minus_cost('U0a84d6de855ff90af62127932c7fde1f', "202105"))


def get_today_date():
    seconds = t.time()
    result = t.localtime(seconds)
    #print(result)
    if result.tm_mon < 10:
        month = '0' + str(result.tm_mon)
    else:
        month = str(result.tm_mon)
    if result.tm_mday < 10:
        day = '0' + str(result.tm_mday)
    else:
        day = str(result.tm_mday)
    today = str(result.tm_year) + month + day
    #print(today)
    return today


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


string = get_today_date()
year = int(string[:4])  # 年
month = int(string[4:6])  # 月
day = int(string[-2:])  # 日
res = last_day_of_month(datetime.date(year, month, day))
lastday = str(res)[-2:]



# 輸入userid和月份得到以後幾天平均可花費金額
def average(userid, types):
    money = income_minus_cost(userid, types)
    left = int(lastday) - day + 1
    avg = round(money / left)
    if  avg > 200 :
        reply = "這個月還剩"+str(money)+"元"+"\n"+"剩下的幾天你平均每一天可以花"+str(avg)+"元"+'\n應該蠻充裕的 恭喜你'
        u = '6362'
        v = "11087940"
    elif 100 <= avg < 200 :
        reply = "這個月還剩"+str(money)+"元"+"\n"+"剩下的幾天你平均每一天可以花" + str(avg) + "元" + '\n加油 省著點用應該能活到月底'
        u = '6362'
        v = '11087933'
    elif 50 <= avg < 100 :
        reply = "這個月還剩"+str(money)+"元"+"\n"+"剩下的幾天你平均每一天可以花" + str(avg) + "元" + '\n哎呀呀 要準備開始吃泡麵囉'
        u = '6362'
        v = '11087937'
    else :
        reply = "哇糟糕 你破產了"+"\n"+"這個月你花超過"+str(money)+"元"
        u = '6362'
        v = '11087938'
    return reply+u+v

#print(average('U0a84d6de855ff90af62127932c7fde1f', "202106"))


def find_row_money(userid, time):
    url2 = 'https://docs.google.com/spreadsheets/d/14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA/export?format=csv'  # 下載連結
    webpage = urllib.request.urlopen(url2)  # 開啟網頁
    data2 = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())  # 讀取資料到data陣列中
    apple = [[i["userid"], i["金額"], i["時間"]] for i in data2]
    i = 0
    b = []
    reply = -2
    while i < len(apple):
        if userid == apple[i][0] and time == apple[i][2][:4]+apple[i][2][5:7]:
            b.append(str(i))
            if len(b) > 0:
                reply = b[0]

        i = i + 1
    return int(reply) + 2
print(find_row_money('U0a84d6de855ff90af62127932c7fde1f', "202106"))
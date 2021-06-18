import csv,requests
import time as t
# coding=utf-8

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

def get_yesterday_date():
    seconds = t.time()
    yesterday_second = seconds - 86400
    #print(yesterday_second)
    result = t.localtime(yesterday_second)
    #print(result)
    if result.tm_mon < 10:
        month = '0' + str(result.tm_mon)
    else:
        month = str(result.tm_mon)
    if result.tm_mday < 10:
        day = '0' + str(result.tm_mday)
    else:
        day = str(result.tm_mday)
    yesterday = str(result.tm_year) + month + day
    #print(yesterday)
    return yesterday

def get_The_day_before_yesterday_date():
    seconds = t.time()
    The_day_before_yesterday_second = seconds - 86400 - 86400
    #print(The_day_before_yesterday_second)
    result = t.localtime(The_day_before_yesterday_second)
    #print(result)
    if result.tm_mon < 10:
        month = '0' + str(result.tm_mon)
    else:
        month = str(result.tm_mon)
    if result.tm_mday < 10:
        day = '0' + str(result.tm_mday)
    else:
        day = str(result.tm_mday)
    The_day_before_yesterday = str(result.tm_year) + month + day
    #print(The_day_before_yesterday)
    return The_day_before_yesterday

def check_date_spend_record(userid, text):
    if '今天' in text:
        date = get_today_date()
        #print(date)
    elif '昨天' in text:
        date = get_yesterday_date()
        #print(date)
    elif '前天' in text:
        date = get_The_day_before_yesterday_date()
        #print(date)
    else:
        date = text.split('花')[0].split('詢')[1]
        #print(date[0:2], date[2:4])
        seconds = t.time()
        result = t.localtime(seconds)
        date = str(result.tm_year) + date
        #print(date)
    if int(date[4:6]) > 12:
        reply = '月份輸入錯誤'
    elif int(date[6:8]) > 31:
        reply = '日期輸入錯誤'
    else:
        reply = check_spend_data_from_date(userid, date)
    return reply

def check_spend_data_from_date(userid, date):
    data = {}
    order = 0
    with requests.Session() as s:
        url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] == userid:
                time = row[4]
                year = time[0:4]
                month = time[5:7]
                day = time[8:10]
                if year == date[0:4] and month == date[4:6] and day == date[6:8]:
                    #print(row)
                    item = row[1]
                    necessity = row[2]
                    amount = row[3]
                    dic = {order: [item, necessity, amount]}
                    #print(dic)
                    order += 1
                    data.update(dic)
            else:
                continue
    #print(data)
    if data == {}:
        reply = '當天沒有任何資料或是日期輸入錯誤'
    else:
        reply = '查詢到{}筆資料'.format(str(order))
        a = '--------------------------------------'
        for i in range(len(data)):
            reply = reply + '\n'+a+'\n{} {}支出 {}元'.format(data[i][0][:2], data[i][1], data[i][2])
    return reply

def check_last_spend_data(userid, text):
    order = text.split('筆')[0].split('上')[1]
    number = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    if order in number:
        a = number[order]
        #print(a)
    else:
        a = int(order)
        #print(a)
    reply = check_last_number_spend_data(userid, a)
    return reply

def check_last_number_spend_data(userid, number):
    data = {}
    order = 0
    with requests.Session() as s:
        url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] == userid:
                #print(row)
                time = row[4]
                year = time[0:4]
                month = time[5:7]
                day = time[8:10]
                hour = time[11:13]
                minutes = time[14:16]
                item = row[1]
                necessity = row[2]
                amount = row[3]
                dic = {order: [year, month, day, hour, minutes, item, necessity, amount]}
                #print(dic)
                order += 1
                data.update(dic)
            else:
                continue
    #print(data)
    if data == {}:
        reply = '查詢不到資料'
    else:
        reply = '資料從新到舊'
        a = '----------------------------------------------------------------'
        for i in range(number):
            k = order - i -1
            reply = reply +'\n'+a+ '\n{}.{}.{} {}:{} {} {}支出 {}元'.format(data[k][0], data[k][1], data[k][2], data[k][3], data[k][4], data[k][5], data[k][6], data[k][7])
    return reply

def check_how_many_records_in_spend_data(userid):
    order = 0
    with requests.Session() as s:
        url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] == userid:
                order = order + 1
            else:
                continue
    reply = '共有{}筆資料'.format(str(order - 1))
    return reply

def check_number_records_in_spend_data(userid, text):
    number = text.split('第')[1].split('筆')[0]
    #print(number)
    data = {}
    order = 0
    with requests.Session() as s:
        url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] == userid:
                #print(row)
                time = row[4]
                year = time[0:4]
                month = time[5:7]
                day = time[8:10]
                hour = time[11:13]
                minutes = time[14:16]
                item = row[1]
                necessity = row[2]
                amount = row[3]
                dic = {order: [year, month, day, hour, minutes, item, necessity, amount]}
                #print(dic)
                order += 1
                data.update(dic)
            else:
                continue
    #print(data)
    if int(number) >= int(order):
        reply = '第{}筆資料不存在'.format(number)
    else:
        reply = '第{}筆資料為\n年分 月份 日期 小時 分鐘 項目 必要性 金額'.format(number)
        reply = reply + '\n{} {} {} {} {} {} {} {}'.format(data[int(number)][0], data[int(number)][1], data[int(number)][2], data[int(number)][3], data[int(number)][4], data[int(number)][5], data[int(number)][6], data[int(number)][7])
    return reply
def check_last_item_spend_data(userid , text):
    order = text.split('筆')[0].split('上')[1]
    number = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    if order in number:
        a = number[order]
        #print(a)
    else:
        a = int(order)
        #print(a)
    b = text.split('筆')[1].split('花')[0]
    reply = check_last_item_from_spend_data(userid, a, b)
    return reply

def check_last_item_from_spend_data(userid, number, item):
    data = {}
    order = 0
    with requests.Session() as s:
        url = 'https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/export?format=csv'
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] == userid and row[1] == item:
                #print(row)
                time = row[4]
                year = time[0:4]
                month = time[5:7]
                day = time[8:10]
                hour = time[11:13]
                minutes = time[14:16]
                necessity = row[2]
                amount = row[3]
                dic = {order: [year, month, day, hour, minutes, necessity, amount]}
                #print(dic)
                order += 1
                data.update(dic)
            else:
                continue
    #print(data)
    if data == {}:
        reply = '查詢不到資料'
    elif number >= order:
        reply = '資料不足{}筆，將呈現{}筆{}花費'.format(number, order, item)
        reply = reply + '資料從新到舊\n年分 月份 日期 小時 分鐘 必要性 金額'
        for i in range(order):
            reply = reply + '\n{} {} {} {} {} {} {}'.format(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6])
    else:
        reply = '將呈現{}筆{}花費，資料從新到舊'.format(number, item)
        a = '--------------------------------------------------------'
        for i in range(number):
            k = order - i -1
            reply = reply +'\n'+a+ '\n{}.{}.{} {}:{} {}支出 {}元'.format(data[k][0], data[k][1], data[k][2], data[k][3], data[k][4], data[k][5], data[k][6])
    return reply
#if __name__ == '__main__':
    #print(check_date_spend_record('U0a84d6de855ff90af62127932c7fde1f', '查詢0612花費'))
    #print(check_spend_data_from_date('U0a84d6de855ff90af62127932c7fde1f', '20210622'))
    #print(get_The_day_before_yesterday_date())
    #print(check_last_spend_data('U0a84d6de855ff90af62127932c7fde1f', '查詢上五筆花費'))
    #print(check_last_number_spend_data('U0a84d6de855ff90af62127932c7fde1f', 5))
    #print(check_how_many_records_in_spend_data('U0a84d6de855ff90af62127932c7fde1f'))
    #print(check_number_records_in_spend_data('U0a84d6de855ff90af62127932c7fde1f', '查詢第4019筆資料'))
    #print(check_last_item_spend_data('U0a84d6de855ff90af62127932c7fde1f', '查詢上5筆飲食花費紀錄'))


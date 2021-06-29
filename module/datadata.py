import glob,time,csv,requests,datetime,urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
# coding=utf-8

#新增雙層字典所使用的函式
def addtwodimdict(thedict, key_a, key_b, val):
  if key_a in thedict:
    thedict[key_a].update({key_b: val})
  else:
    thedict.update({key_a:{key_b: val}})
#新增三層字典所使用的函式
def addthreedimdict(thedict, key_a, key_b,key_c, val):
  if key_a in thedict:
      if key_b in thedict[key_a]:
        thedict[key_a][key_b].update({key_c: val})
      elif key_b not in thedict[key_a]:
        thedict[key_a].update({key_b: {key_c: val}})
  elif key_a not in thedict:
      thedict.update({key_a:{key_b:{key_c: val}}})
#圖片排版
def identify_axes(ax_dict, fontsize=48):
    """
    Helper to identify the Axes in the examples below.

    Draws the label in a large font in the center of the Axes.

    Parameters
    ----------
    ax_dict : dict[str, Axes]
        Mapping between the title / label and the Axes.
    fontsize : int, optional
        How big the label should be.
    """
    kw = dict(ha="center", va="center", fontsize=fontsize, color="darkgrey")
    #for k, ax in ax_dict.items():
        #ax.text(0.5, 0.5, k, transform=ax.transAxes, **kw)
def get_spend_csv():
    url = 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)

def get_all_user_id_list_from_spend_csv_url(url):
    user = []
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] != 'userid' and row[0] not in user:
                user.append(row[0])
            else:
                continue
            print(user)
    return user

def get_user_data_from_spend_csv_url(userid, url):
    data ={}
    order = 0
    with requests.Session() as s:
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
                seconds = time[17:19]
                item = row[1]
                necessity = row[2]
                amount = row[3]
                dic = {order: [year, month, day, hour, minutes, seconds, item, necessity, amount]}
                #print(dic)
                order += 1
                data.update(dic)
            else:
                continue
    #print(data)
    return data

def creat_user_csv_data(userid, data):
    path = '{}.csv'.format(userid)
    with open(path, 'w',  newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        csv_head = [userid, "年份", '月份', '日期', '小時', '分鐘', '秒數', '項目', '必要性', '金額']
        writer.writerow(csv_head)
    with open(path, 'a+', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        for i in range(len(data)):
            list = [i]
            for j in range(len(data[i])):
                list.append(data[i][j])
            writer.writerow(list)

def creat_all_user_spend_csv_data(url):
    userid_list = get_all_user_id_list_from_spend_csv_url(url)
    #print(userid_list)
    for i in range(len(userid_list)):
        userid = userid_list[i]
        #print(userid)
        data = get_user_data_from_spend_csv_url(userid, url)
        a=creat_user_csv_data(userid, data)
    return a

def get_income_csv():
    url = 'https://docs.google.com/spreadsheets/d/1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4/export?format=cs'
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)

def get_all_user_id_list_from_income_csv_url(url):
    user = []
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] != 'userid' and row[0] not in user:
                user.append(row[0])
            else:
                continue
            print(user)
    return user

def get_user_data_from_income_csv_url(userid, url):
    data ={}
    order = 0
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if row[0] == userid:
                print(row)

                dic = {order: [year, month, day, hour, minutes, seconds, item, necessity, amount]}
                print(dic)
                order += 1
                data.update(dic)
            else:
                continue
    print(data)
    return data
#每一日為key,每日總金額為value
def spend_sum_of_abs_day(userid, url):
    dict={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[0]+i[1]+i[2]
        if day in dict:
            dict[day]+=int(i[8])
        else:
            dict[day]=int(i[8])
    return dict
#每一月為key,每月總金額為value
def spend_sum_of_abs_month(userid, url):
    dict={}
    for key,value in spend_sum_of_abs_day(userid, url).items():
        if key[0:6] in dict:
            dict[key[0:6]]+=value
        else:
            dict[key[0:6]]=value
    return dict

#每一年為key,每年總金額為value
def spend_sum_of_abs_year(userid, url):
    dict={}
    for key, value in spend_sum_of_abs_day(userid, url).items():
        if key[0:4] in dict:
            dict[key[0:4]] += value
        else:
            dict[key[0:4]] = value
    return dict
#每一年為key,每年總金額/每年登錄月數為value
def spend_sum_of_abs_year_month_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_sum_of_abs_month(userid, url).keys():
        if i[0:4] in dict2:
            dict2[i[0:4]]+=1
        else:
            dict2[i[0:4]]=1
    for key1, value1 in spend_sum_of_abs_year(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一年為key,每年總金額/每年登錄日數為value
def spend_sum_of_abs_year_day_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_sum_of_abs_day(userid, url).keys():
        if i[0:4] in dict2:
            dict2[i[0:4]]+=1
        else:
            dict2[i[0:4]]=1
    for key1, value1 in spend_sum_of_abs_year(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一月為key,每月總金額/每月登錄日數為value
def spend_sum_of_abs_month_day_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_sum_of_abs_day(userid, url).keys():
        if i[0:6] in dict2:
            dict2[i[0:6]]+=1
        else:
            dict2[i[0:6]]=1
    for key1, value1 in spend_sum_of_abs_month(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一日為key,每日必要總金額為value
def spend_necessary_sum_of_abs_day(userid, url):
    dict1={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[0]+i[1]+i[2]
        if (day in dict1) and (i[7]=='必要'):
            dict1[day]+=int(i[8])
        elif (day not in dict1) and(i[7]=='必要'):
            dict1[day]=int(i[8])
    return dict1
#每一日為key,每日不必要總金額為value
def spend_unnecessary_sum_of_abs_day(userid, url):
    dict1={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[0]+i[1]+i[2]
        if (day in dict1) and (i[7]=='不必要'):
            dict1[day]+=int(i[8])
        elif (day not in dict1) and(i[7]=='不必要'):
            dict1[day]=int(i[8])
    return dict1
#每一月為key,每月必要總金額為value
def spend_necessary_sum_of_abs_month(userid, url):
    dict={}
    for key,value in spend_necessary_sum_of_abs_day(userid, url).items():
        if (key[0:6] in dict):
            dict[key[0:6]]+=value
        elif (key[0:6] not in dict):
            dict[key[0:6]]=value
    return dict
#每一月為key,每月不必要總金額為value
def spend_unnecessary_sum_of_abs_month(userid, url):
    dict={}
    for key,value in spend_unnecessary_sum_of_abs_day(userid, url).items():
        if (key[0:6] in dict) :
            dict[key[0:6]]+=value
        elif (key[0:6] not in dict) :
            dict[key[0:6]]=value
    return dict
#每一年為key,每年必要總金額為value
def spend_necessary_sum_of_abs_year(userid, url):
    dict={}
    for key, value in spend_necessary_sum_of_abs_day(userid, url).items():
        if (key[0:4] in dict) :
            dict[key[0:4]] += value
        elif (key[0:4] not in dict) :
            dict[key[0:4]] = value
    return dict
#每一年為key,每年不必要總金額為value
def spend_unnecessary_sum_of_abs_year(userid, url):
    dict={}
    for key, value in spend_unnecessary_sum_of_abs_day(userid, url).items():
        if (key[0:4] in dict) :
            dict[key[0:4]] += value
        elif (key[0:4] not in dict) :
            dict[key[0:4]] = value
    return dict
#每一年為key,每年必要總金額/每年登錄月數為value
def spend_necessary_sum_of_abs_year_month_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_necessary_sum_of_abs_month(userid, url).keys():
        if i[0:4] in dict2:
            dict2[i[0:4]]+=1
        else:
            dict2[i[0:4]]=1
    for key1, value1 in spend_necessary_sum_of_abs_year(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一年為key,每年不必要總金額/每年登錄月數為value
def spend_unnecessary_sum_of_abs_year_month_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_unnecessary_sum_of_abs_month(userid, url).keys():
        if i[0:4] in dict2:
            dict2[i[0:4]]+=1
        else:
            dict2[i[0:4]]=1
    for key1, value1 in spend_unnecessary_sum_of_abs_year(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一年為key,每年必要總金額/每年登錄日數為value
def spend_necessary_sum_of_abs_year_day_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_necessary_sum_of_abs_day(userid, url).keys():
        if i[0:4] in dict2:
            dict2[i[0:4]]+=1
        else:
            dict2[i[0:4]]=1
    for key1, value1 in spend_necessary_sum_of_abs_year(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一年為key,每年不必要總金額/每年登錄日數為value
def spend_unnecessary_sum_of_abs_year_day_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_unnecessary_sum_of_abs_day(userid, url).keys():
        if i[0:4] in dict2:
            dict2[i[0:4]]+=1
        else:
            dict2[i[0:4]]=1
    for key1, value1 in spend_unnecessary_sum_of_abs_year(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一月為key,每月必要總金額/每月登錄日數為value
def spend_necessary_sum_of_abs_month_day_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_necessary_sum_of_abs_day(userid, url).keys():
        if i[0:6] in dict2:
            dict2[i[0:6]]+=1
        else:
            dict2[i[0:6]]=1
    for key1, value1 in spend_necessary_sum_of_abs_month(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3

#每一月為key,每月不必要總金額/每月登錄日數為value
def spend_unnecessary_sum_of_abs_month_day_average(userid, url):
    dict2={}
    dict3 = {}
    for i in spend_unnecessary_sum_of_abs_day(userid, url).keys():
        if i[0:6] in dict2:
            dict2[i[0:6]]+=1
        else:
            dict2[i[0:6]]=1
    for key1, value1 in spend_unnecessary_sum_of_abs_month(userid, url).items():
        dict3[key1]=float(value1)/float(dict2[key1])
    return  dict3
#每一日為key,每日項目總金額為value(兩層)(日->項目)
def spend_item_sum_of_abs_day(userid, url):
    dict1={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[0]+i[1]+i[2]
        if day in dict1:
            if i[6] in dict1[day]:
                a=dict1[day][i[6]]+int(i[8])
                addtwodimdict(dict1, day, i[6], a)
                #print(dict1)
            elif i[6] not in dict1[day]:
                addtwodimdict(dict1, day, i[6], int(i[8]))
                #print(dict1)
        elif day not in dict1 :
            addtwodimdict(dict1, day, i[6], int(i[8]))
            #print(dict1)
    return dict1
#每一月為key,每月項目總金額為value(兩層)(月->項目)
def spend_item_sum_of_abs_month(userid, url):
    dict = {}
    for key1, value1 in spend_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            if key1[0:6] in dict:
                if key2 in dict[key1[0:6]]:
                    a=dict[key1[0:6]][key2] + value2
                    addtwodimdict(dict, key1[0:6], key2, a)
                    print(dict)
                elif key2 not in dict[key1[0:6]]:
                    addtwodimdict(dict, key1[0:6], key2, value2)
                    print(dict)
            elif key1[0:6] not in dict:
                addtwodimdict(dict, key1[0:6], key2, value2)
                print(dict)
    return dict
#每一年為key,每年項目總金額為value(兩層)(年->項目)
def spend_item_sum_of_abs_year(userid, url):
    dict = {}
    for key1, value1 in spend_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            if key1[0:4] in dict:
                if key2 in dict[key1[0:4]]:
                    a=dict[key1[0:4]][key2] + value2
                    addtwodimdict(dict, key1[0:4], key2, a)
                    print(dict)
                elif key2 not in dict[key1[0:4]]:
                    addtwodimdict(dict, key1[0:4], key2, value2)
                    print(dict)
            elif key1[0:4] not in dict:
                addtwodimdict(dict, key1[0:4], key2, value2)
                print(dict)
    return dict
#每一年為key,每年項目總金額/每年登錄月數為value(兩層)(月->項目)
def spend_item_sum_of_abs_year_month_average(userid, url):
    dict2={}
    dict3 = {}
    for key1,value1 in spend_item_sum_of_abs_month(userid, url).items():
        for key2, value2 in value1.items():
            if key1[0:4] in dict2:
                if key2 in dict2[key1[0:4]]:
                    b=dict2[key1[0:4]][key2]+1
                    addtwodimdict(dict2, key1[0:4], key2, b)
                    print(dict2)
                elif key2 not in dict2[key1[0:4]]:
                    addtwodimdict(dict2, key1[0:4], key2, 1)
                    print(dict2)
            elif key1[0:4] not in dict2:
                addtwodimdict(dict2, key1[0:4], key2, 1)
                print(dict2)
    for key3, value3 in spend_item_sum_of_abs_year(userid, url).items():
        for key4, value4 in value3.items():
            c=float(value4)/float(dict2[key3][key4])
            addtwodimdict(dict3, key3, key4,c)
    return  dict3
#每一年為key,每年項目總金額/每年登錄日數為value(兩層)(年->項目)
def spend_item_sum_of_abs_year_day_average(userid, url):
    dict2 = {}
    dict3 = {}
    for key1, value1 in spend_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            if key1[0:4] in dict2:
                if key2 in dict2[key1[0:4]]:
                    b = dict2[key1[0:4]][key2] + 1
                    addtwodimdict(dict2, key1[0:4], key2, b)
                    print(dict2)
                elif key2 not in dict2[key1[0:4]]:
                    addtwodimdict(dict2, key1[0:4], key2, 1)
                    print(dict2)
            elif key1[0:4] not in dict2:
                addtwodimdict(dict2, key1[0:4], key2, 1)
                print(dict2)
    for key3, value3 in spend_item_sum_of_abs_year(userid, url).items():
        for key4, value4 in value3.items():
            c = float(value4) / float(dict2[key3][key4])
            addtwodimdict(dict3, key3, key4, c)
    return dict3
#每一月為key,每月項目總金額/每月登錄日數為value(兩層)(月->項目)
def spend_item_sum_of_abs_month_day_average(userid, url):
    dict2 = {}
    dict3 = {}
    for key1, value1 in spend_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            if key1[0:6] in dict2:
                if key2 in dict2[key1[0:6]]:
                    b = dict2[key1[0:6]][key2] + 1
                    addtwodimdict(dict2, key1[0:6], key2, b)
                    print(dict2)
                elif key2 not in dict2[key1[0:6]]:
                    addtwodimdict(dict2, key1[0:6], key2, 1)
                    print(dict2)
            elif key1[0:6] not in dict2:
                addtwodimdict(dict2, key1[0:6], key2, 1)
                print(dict2)
    for key3, value3 in spend_item_sum_of_abs_month(userid, url).items():
        for key4, value4 in value3.items():
            c = float(value4) / float(dict2[key3][key4])
            addtwodimdict(dict3, key3, key4, c)
    return dict3
#每一日為key,每日必要與不必要項目總金額為value(三層)(日->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_abs_day(userid, url):
    dict1={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[0]+i[1]+i[2]
        if day in dict1:
            if i[7] in dict1[day]:
                if i[6] in dict1[day][i[7]]:
                    a=dict1[day][i[7]][i[6]]+int(i[8])
                    addthreedimdict(dict1, day,i[7],i[6], a)
                    #print(dict1)
                elif i[6] not in dict1[day][i[7]]:
                    addthreedimdict(dict1, day,i[7], i[6], int(i[8]))
                    #print(dict1)
            elif i[7] not in dict1[day]:
                addthreedimdict(dict1, day, i[7], i[6], int(i[8]))
        elif day not in dict1 :
            addthreedimdict(dict1, day,i[7], i[6], int(i[8]))
            #print(dict1)
    return dict1
#每一月為key,每月必要與不必要項目總金額為value(三層)(月->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url):
    dict = {}
    for key1, value1 in spend_necessary_and_unnecessary_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[0:6] in dict:
                    if key2 in dict[key1[0:6]]:
                        if key3 in dict[key1[0:6]][key2]:
                            a=dict[key1[0:6]][key2][key3] + value3
                            addthreedimdict(dict, key1[0:6], key2,key3,a)
                            print(dict)
                        elif key3 not in dict[key1[0:6]][key2]:
                            addthreedimdict(dict, key1[0:6], key2, key3,value3 )
                            print(dict)
                    elif key2 not in dict[key1[0:6]]:
                        addthreedimdict(dict, key1[0:6], key2, key3, value3)
                        print(dict)
                elif key1[0:6] not in dict:
                    addthreedimdict(dict, key1[0:6], key2, key3,value3 )
                    print(dict)
    return dict
#每一年為key,每年必要與不必要項目總金額為value(三層)(年->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_abs_year(userid, url):
    dict = {}
    for key1, value1 in spend_necessary_and_unnecessary_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[0:4] in dict:
                    if key2 in dict[key1[0:4]]:
                        if key3 in dict[key1[0:4]][key2]:
                            a = dict[key1[0:4]][key2][key3] + value3
                            addthreedimdict(dict, key1[0:4], key2, key3, a)
                            print(dict)
                        elif key3 not in dict[key1[0:4]][key2]:
                            addthreedimdict(dict, key1[0:4], key2, key3, value3)
                            print(dict)
                    elif key2 not in dict[key1[0:4]]:
                        addthreedimdict(dict, key1[0:4], key2, key3, value3)
                        print(dict)
                elif key1[0:4] not in dict:
                    addthreedimdict(dict, key1[0:4], key2, key3, value3)
                    print(dict)
    return dict
#每一年為key,每年必要與不必要項目總金額/每年登錄月數為value(三層)(年->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_abs_year_month_average(userid, url):
    dict2={}
    dict3 = {}
    for key1,value1 in spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[0:4] in dict2:
                    if key2 in dict2[key1[0:4]]:
                        if key3 in dict2[key1[0:4]][key2]:
                            b=dict2[key1[0:4]][key2][key3]+1
                            addthreedimdict(dict2, key1[0:4], key2,key3, b)
                            print(dict2)
                        elif key3 not in dict2[key1[0:4]][key2]:
                            addthreedimdict(dict2, key1[0:4], key2,key3, 1)
                            print(dict2)
                    elif key2 not in dict2[key1[0:4]]:
                        addthreedimdict(dict2, key1[0:4], key2, key3, 1)
                        print(dict2)
                elif key1[0:4] not in dict2:
                    addthreedimdict(dict2, key1[0:4], key2, key3, 1)
                    print(dict2)
    for key4, value4 in spend_necessary_and_unnecessary_item_sum_of_abs_year(userid, url).items():
        for key5, value5 in value4.items():
            for key6, value6 in value5.items():
                c=float(value6)/float(dict2[key4][key5][key6])
                addthreedimdict(dict3, key4, key5,key6,c)
    return  dict3
#每一年為key,每年必要與不必要項目總金額/每年登錄日數為value(三層)(年->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_abs_year_day_average(userid, url):
    dict2 = {}
    dict3 = {}
    for key1, value1 in spend_necessary_and_unnecessary_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[0:4] in dict2:
                    if key2 in dict2[key1[0:4]]:
                        if key3 in dict2[key1[0:4]][key2]:
                            b = dict2[key1[0:4]][key2][key3] + 1
                            addthreedimdict(dict2, key1[0:4], key2, key3, b)
                            print(dict2)
                        elif key3 not in dict2[key1[0:4]][key2]:
                            addthreedimdict(dict2, key1[0:4], key2, key3, 1)
                            print(dict2)
                    elif key2 not in dict2[key1[0:4]]:
                        addthreedimdict(dict2, key1[0:4], key2, key3, 1)
                        print(dict2)
                elif key1[0:4] not in dict2:
                    addthreedimdict(dict2, key1[0:4], key2, key3, 1)
                    print(dict2)
    for key4, value4 in spend_necessary_and_unnecessary_item_sum_of_abs_year(userid, url).items():
        for key5, value5 in value4.items():
            for key6, value6 in value5.items():
                c = float(value6) / float(dict2[key4][key5][key6])
                addthreedimdict(dict3, key4, key5, key6, c)
    return dict3
#每一月為key,每月必要與不必要項目總金額/每月登錄日數為value(三層)(月->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_abs_month_day_average(userid, url):
    dict2 = {}
    dict3 = {}
    for key1, value1 in spend_necessary_and_unnecessary_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[0:6] in dict2:
                    if key2 in dict2[key1[0:6]]:
                        if key3 in dict2[key1[0:6]][key2]:
                            b = dict2[key1[0:6]][key2][key3] + 1
                            addthreedimdict(dict2, key1[0:6], key2, key3, b)
                            print(dict2)
                        elif key3 not in dict2[key1[0:6]][key2]:
                            addthreedimdict(dict2, key1[0:6], key2, key3, 1)
                            print(dict2)
                    elif key2 not in dict2[key1[0:6]]:
                        addthreedimdict(dict2, key1[0:6], key2, key3, 1)
                        print(dict2)
                elif key1[0:6] not in dict2:
                    addthreedimdict(dict2, key1[0:6], key2, key3, 1)
                    print(dict2)
    for key4, value4 in spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url).items():
        for key5, value5 in value4.items():
            for key6, value6 in value5.items():
                c = float(value6) / float(dict2[key4][key5][key6])
                addthreedimdict(dict3, key4, key5, key6, c)
    return dict3
#每一相同日為key,每一相同日總金額為value
def spend_sum_of_same_day(userid, url):
    dict={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[2]
        if day in dict:
            dict[day]+=int(i[8])
        else:
            dict[day]=int(i[8])
    return dict
#每一相同月為key,每一相同月總金額為value
def spend_sum_of_same_month(userid, url):
    dict={}
    for key,value in spend_sum_of_abs_day(userid, url).items():
        if key[4:6] in dict:
            dict[key[4:6]]+=value
        else:
            dict[key[4:6]]=value
    return dict
#每一相同日為key,每一相同日總金額/次數為value
def spend_sum_of_same_day_average(userid, url):
    dict1={}
    dict2={}
    for i in spend_sum_of_abs_day(userid, url).keys():
        day=i[6:]
        if day in dict1:
            dict1[day]+=1
        else:
            dict1[day]=1
    for key,value in spend_sum_of_same_day(userid, url).items():
        dict2[key]=float(value)/float(dict1[key])
    return dict2
#每一相同月為key,每一相同月總金額/次數為value
def spend_sum_of_same_month_average(userid, url):
    dict1 = {}
    dict2 = {}
    for i in spend_sum_of_abs_month(userid, url).keys():
        month = i[4:]
        if month in dict1:
            dict1[month] += 1
        else:
            dict1[month] = 1
    for key, value in spend_sum_of_same_month(userid, url).items():
        dict2[key] = float(value) / float(dict1[key])
    return dict2
#每一相同日為key,每一相同日必要總金額為value
def spend_necessary_sum_of_same_day(userid, url):
    dict={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[2]
        if (day in dict) and (i[7]=='必要'):
            dict[day]+=int(i[8])
        elif (day not in dict) and (i[7]=='必要'):
            dict[day]=int(i[8])
    return dict
#每一相同日為key,每一相同日不必要總金額為value
def spend_unnecessary_sum_of_same_day(userid, url):
    dict={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[2]
        if (day in dict) and (i[7]=='不必要'):
            dict[day]+=int(i[8])
        elif (day not in dict) and (i[7]=='不必要'):
            dict[day]=int(i[8])
    return dict
#每一相同月為key,每一相同月必要總金額為value
def spend_necessary_sum_of_same_month(userid, url):
    dict = {}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        month = i[1]
        if (month in dict) and (i[7] == '必要'):
            dict[month] += int(i[8])
        elif (month not in dict) and (i[7] == '必要'):
            dict[month] = int(i[8])
    return dict
#每一相同月為key,每一相同月不必要總金額為value
def spend_unnecessary_sum_of_same_month(userid, url):
    dict = {}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        month = i[1]
        if (month in dict) and (i[7] == '不必要'):
            dict[month] += int(i[8])
        elif (month not in dict) and (i[7] == '不必要'):
            dict[month] = int(i[8])
    return dict
#每一相同日為key,每一相同日必要總金額/次數為value
def spend_necessary_sum_of_same_day_average(userid, url):
    dict1 = {}
    dict2 = {}
    for i in spend_necessary_sum_of_abs_day(userid, url).keys():
        day = i[6:]
        if (day in dict1) :
            dict1[day] += 1
        else:
            dict1[day] = 1
    for key, value in spend_necessary_sum_of_same_day(userid, url).items():
        dict2[key] = float(value) / float(dict1[key])
    return dict2
#每一相同日為key,每一相同日不必要總金額/次數為value
def spend_unnecessary_sum_of_same_day_average(userid, url):
    dict1 = {}
    dict2 = {}
    for i in spend_unnecessary_sum_of_abs_day(userid, url).keys():
        day = i[6:]
        if (day in dict1):
            dict1[day] += 1
        else:
            dict1[day] = 1
    for key, value in spend_unnecessary_sum_of_same_day(userid, url).items():
        dict2[key] = float(value) / float(dict1[key])
    return dict2
#每一相同月為key,每一相同月必要總金額/次數為value
def spend_necessary_sum_of_same_month_average(userid, url):
    dict1 = {}
    dict2 = {}
    for i in spend_necessary_sum_of_abs_month(userid, url).keys():
        day = i[4:]
        if (day in dict1):
            dict1[day] += 1
        else:
            dict1[day] = 1
    for key, value in spend_necessary_sum_of_same_month(userid, url).items():
        dict2[key] = float(value) / float(dict1[key])
    return dict2
#每一相同月為key,每一相同月不必要總金額/次數為value
def spend_unnecessary_sum_of_same_month_average(userid, url):
    dict1 = {}
    dict2 = {}
    for i in spend_unnecessary_sum_of_abs_month(userid, url).keys():
        day = i[4:]
        if (day in dict1):
            dict1[day] += 1
        else:
            dict1[day] = 1
    for key, value in spend_unnecessary_sum_of_same_month(userid, url).items():
        dict2[key] = float(value) / float(dict1[key])
    return dict2
#每一相同日為key,每一相同日項目總金額為value(兩層)(日->項目)
def spend_item_sum_of_same_day(userid, url):
    dict = {}
    for key1, value1 in spend_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            if key1[6:] in dict:
                if key2 in dict[key1[6:]]:
                    a = dict[key1[6:]][key2] + value2
                    addtwodimdict(dict, key1[6:], key2, a)
                    print(dict)
                elif key2 not in dict[key1[6:]]:
                    addtwodimdict(dict, key1[6:], key2, value2)
                    print(dict)
            elif key1[6:] not in dict:
                addtwodimdict(dict, key1[6:], key2, value2)
                print(dict)
    return dict
#每一相同月為key,每一相同月項目總金額為value(兩層)(月->項目)
def spend_item_sum_of_same_month(userid, url):
    dict = {}
    for key1, value1 in spend_item_sum_of_abs_month(userid, url).items():
        for key2, value2 in value1.items():
            if key1[4:] in dict:
                if key2 in dict[key1[4:]]:
                    a=dict[key1[4:]][key2] + value2
                    addtwodimdict(dict, key1[4:], key2, a)
                    print(dict)
                elif key2 not in dict[key1[4:]]:
                    addtwodimdict(dict, key1[4:], key2, value2)
                    print(dict)
            elif key1[4:] not in dict:
                addtwodimdict(dict, key1[4:], key2, value2)
                print(dict)
    return dict
#每一相同日為key,每一相同日項目總金額/次數為value(兩層)(日->項目)
def spend_item_sum_of_same_day_average(userid, url):
    dict1 = {}
    dict2 = {}
    for key1, value1 in spend_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            if key1[6:] in dict1:
                if key2 in dict1[key1[6:]]:
                    a = dict1[key1[6:]][key2] + 1
                    addtwodimdict(dict1, key1[6:], key2, a)
                    print(dict1)
                elif key2 not in dict1[key1[6:]]:
                    addtwodimdict(dict1, key1[6:], key2, 1)
                    print(dict1)
            elif key1[6:] not in dict1:
                addtwodimdict(dict1, key1[6:], key2, 1)
                print(dict1)
    for key3, value3 in spend_item_sum_of_same_day(userid, url).items():
        for key4, value4 in value3.items():
            b= float(value4) / float(dict1[key3][key4])
            addtwodimdict(dict2, key3, key4, b)
            print(dict2)
    return dict2
#每一相同月為key,每一相同月項目總金額/次數為value(兩層)(月->項目)
def spend_item_sum_of_same_month_average(userid, url):
    dict1 = {}
    dict2 = {}
    for key1, value1 in spend_item_sum_of_abs_month(userid, url).items():
        for key2, value2 in value1.items():
            if key1[4:] in dict1:
                if key2 in dict1[key1[4:]]:
                    a = dict1[key1[4:]][key2] + 1
                    addtwodimdict(dict1, key1[4:], key2, a)
                    print(dict1)
                elif key2 not in dict1[key1[4:]]:
                    addtwodimdict(dict1, key1[4:], key2, 1)
                    print(dict1)
            elif key1[4:] not in dict1:
                addtwodimdict(dict1, key1[4:], key2, 1)
                print(dict1)
    for key3, value3 in spend_item_sum_of_same_month(userid, url).items():
        for key4, value4 in value3.items():
            b= float(value4) / float(dict1[key3][key4])
            addtwodimdict(dict2, key3, key4, b)
            print(dict2)
    return dict2
#每一相同日為key,每一相同日必要與不必要項目總金額為value(三層)(日->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_same_day(userid, url):
    dict1={}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        day=i[2]
        if day in dict1:
            if i[7] in dict1[day]:
                if i[6] in dict1[day][i[7]]:
                    a=dict1[day][i[7]][i[6]]+int(i[8])
                    addthreedimdict(dict1, day,i[7],i[6], a)
                    #print(dict1)
                elif i[6] not in dict1[day][i[7]]:
                    addthreedimdict(dict1, day,i[7], i[6], int(i[8]))
                    #print(dict1)
            elif i[7] not in dict1[day]:
                addthreedimdict(dict1, day, i[7], i[6], int(i[8]))
        elif day not in dict1 :
            addthreedimdict(dict1, day,i[7], i[6], int(i[8]))
            #print(dict1)
    return dict1
#每一相同月為key,每一相同月必要與不必要項目總金額為value(三層)(月->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_same_month(userid, url):
    dict1 = {}
    for i in get_user_data_from_spend_csv_url(userid, url).values():
        month = i[1]
        if month in dict1:
            if i[7] in dict1[month]:
                if i[6] in dict1[month][i[7]]:
                    a = dict1[month][i[7]][i[6]] + int(i[8])
                    addthreedimdict(dict1, month, i[7], i[6], a)
                    # print(dict1)
                elif i[6] not in dict1[month][i[7]]:
                    addthreedimdict(dict1, month, i[7], i[6], int(i[8]))
                    # print(dict1)
            elif i[7] not in dict1[month]:
                addthreedimdict(dict1,month, i[7], i[6], int(i[8]))
        elif month not in dict1:
            addthreedimdict(dict1, month, i[7], i[6], int(i[8]))
            # print(dict1)
    return dict1
#每一相同日為key,每一相同日必要與不必要項目總金額/次數為value(三層)(日->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_same_day_average(userid, url):
    dict2 = {}
    dict3 = {}
    for key1, value1 in spend_necessary_and_unnecessary_item_sum_of_abs_day(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[6:] in dict2:
                    if key2 in dict2[key1[6:]]:
                        if key3 in dict2[key1[6:]][key2]:
                            b = dict2[key1[6:]][key2][key3] + 1
                            addthreedimdict(dict2, key1[6:], key2, key3, b)
                            print(dict2)
                        elif key3 not in dict2[key1[6:]][key2]:
                            addthreedimdict(dict2, key1[6:], key2, key3, 1)
                            print(dict2)
                    elif key2 not in dict2[key1[6:]]:
                        addthreedimdict(dict2, key1[6:], key2, key3, 1)
                        print(dict2)
                elif key1[6:] not in dict2:
                    addthreedimdict(dict2, key1[6:], key2, key3, 1)
                    print(dict2)
    for key4, value4 in spend_necessary_and_unnecessary_item_sum_of_same_day(userid, url).items():
        for key5, value5 in value4.items():
            for key6, value6 in value5.items():
                c = float(value6) / float(dict2[key4][key5][key6])
                addthreedimdict(dict3, key4, key5, key6, c)
    return dict3
#每一相同月為key,每一相同月必要與不必要項目總金額/次數為value(三層)(月->必要性->項目)
def spend_necessary_and_unnecessary_item_sum_of_same_month_average(userid, url):
    dict2 = {}
    dict3 = {}
    for key1, value1 in spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url).items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                if key1[4:] in dict2:
                    if key2 in dict2[key1[4:]]:
                        if key3 in dict2[key1[4:]][key2]:
                            b = dict2[key1[4:]][key2][key3] + 1
                            addthreedimdict(dict2, key1[4:], key2, key3, b)
                            print(dict2)
                        elif key3 not in dict2[key1[4:]][key2]:
                            addthreedimdict(dict2, key1[4:], key2, key3, 1)
                            print(dict2)
                    elif key2 not in dict2[key1[4:]]:
                        addthreedimdict(dict2, key1[4:], key2, key3, 1)
                        print(dict2)
                elif key1[6:] not in dict2:
                    addthreedimdict(dict2, key1[4:], key2, key3, 1)
                    print(dict2)
    for key4, value4 in spend_necessary_and_unnecessary_item_sum_of_same_month(userid, url).items():
        for key5, value5 in value4.items():
            for key6, value6 in value5.items():
                c = float(value6) / float(dict2[key4][key5][key6])
                addthreedimdict(dict3, key4, key5, key6, c)
    return dict3
#每一相同月為key,每一相同月(不包含今年)之每日總金額為value(兩層)(月->日)
def spend_sum_of_same_month_everyday(userid, url):
    dict={}
    day_list=[]
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key,value in spend_sum_of_abs_day(userid, url).items():
        if key[4:6] in dict and key[0:4]!=day_list[-1][0:4]:
            if key[6:] in dict[key[4:6]] :
                a=dict[key[4:6]][key[6:]]+value
                addtwodimdict(dict, key[4:6], key[6:], a)
                print(dict)
            elif key[6:] not in dict[key[4:6]]:
                addtwodimdict(dict, key[4:6], key[6:],value)
                print(dict)
        elif key[4:6] not in dict and key[0:4]!=day_list[-1][0:4]:
            addtwodimdict(dict, key[4:6], key[6:], value)
            print(dict)
    return dict
#每一相同月為key,每一相同月(不包含今年)之每日總金額/次數為value(兩層)(月->日)
def spend_sum_of_same_month_everyday_average(userid, url):
    dict1={}
    dict2={}
    day_list = []
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        if key1[4:6] in dict1 and key1[0:4] != day_list[-1][0:4]:
            if key1[6:] in dict1[key1[4:6]]:
                a = dict1[key1[4:6]][key1[6:]] + 1
                addtwodimdict(dict1, key1[4:6], key1[6:], a)
                print(dict1)
            elif key1[6:] not in dict1[key1[4:6]]:
                addtwodimdict(dict1, key1[4:6], key1[6:], 1)
                print(dict1)
        elif key1[4:6] not in dict1 and key1[0:4] != day_list[-1][0:4]:
            addtwodimdict(dict1, key1[4:6], key1[6:], 1)
            print(dict1)
    for key2,value2 in spend_sum_of_same_month_everyday(userid, url).items():
        for key3, value3 in value2.items():
            b=float(value3)/float(dict1[key2][key3])
            addtwodimdict(dict2, key2, key3,b)
    return dict2
#每一相同月為key,每一相同月平均金額(不包含今年)/次數為value
def spend_sum_of_same_month_day_average(userid, url):
    dict1 = {}
    dict2 = {}
    dict3 = {}
    day_list = []
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key1 in spend_sum_of_abs_month_day_average(userid, url).keys():
        if key1[4:6]in dict1 and key1[0:4]!=day_list[-1][0:4]:
            dict1[key1[4:6]] += 1
        else:
            dict1[key1[4:6]] = 1
    for key2,value2 in spend_sum_of_abs_month_day_average(userid, url).items():
        if key2[4:6] in dict2 and key2[0:4] != day_list[-1][0:4]:
            dict2[key2[4:6]] += value2
        elif key2[4:6] not in dict2 and key2[0:4] != day_list[-1][0:4]:
            dict2[key2[4:6]] = value2
    for key3, value3 in dict2.items():
        dict3[key3] = float(value3) / float(dict1[key3])
    return dict3
#每一相同月為key,每一相同月(不包含今年)之每日必要總金額為value(兩層)(月->日)
def spend_necessary_sum_of_same_month_everyday(userid, url):
    dict={}
    day_list=[]
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key,value in spend_necessary_sum_of_abs_day(userid, url).items():
        if key[4:6] in dict and key[0:4]!=day_list[-1][0:4]:
            if key[6:] in dict[key[4:6]] :
                a=dict[key[4:6]][key[6:]]+value
                addtwodimdict(dict, key[4:6], key[6:], a)
                print(dict)
            elif key[6:] not in dict[key[4:6]]:
                addtwodimdict(dict, key[4:6], key[6:],value)
                print(dict)
        elif key[4:6] not in dict and key[0:4]!=day_list[-1][0:4]:
            addtwodimdict(dict, key[4:6], key[6:], value)
            print(dict)
    return dict
#每一相同月為key,每一相同月(不包含今年)之每日必要總金額/次數為value(兩層)(月->日)
def spend_necessary_sum_of_same_month_everyday_average(userid, url):
    dict1={}
    dict2={}
    day_list = []
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key1 in spend_necessary_sum_of_abs_day(userid, url).keys():
        if key1[4:6] in dict1 and key1[0:4] != day_list[-1][0:4]:
            if key1[6:] in dict1[key1[4:6]]:
                a = dict1[key1[4:6]][key1[6:]] + 1
                addtwodimdict(dict1, key1[4:6], key1[6:], a)
                print(dict1)
            elif key1[6:] not in dict1[key1[4:6]]:
                addtwodimdict(dict1, key1[4:6], key1[6:], 1)
                print(dict1)
        elif key1[4:6] not in dict1 and key1[0:4] != day_list[-1][0:4]:
            addtwodimdict(dict1, key1[4:6], key1[6:], 1)
            print(dict1)
    for key2,value2 in spend_necessary_sum_of_same_month_everyday(userid, url).items():
        for key3, value3 in value2.items():
            b=float(value3)/float(dict1[key2][key3])
            addtwodimdict(dict2, key2, key3,b)
    return dict2
#每一相同月為key,每一相同月必須平均必要金額(不包含今年)/次數為value
def spend_necessary_sum_of_same_month_day_average(userid, url):
    dict1 = {}
    dict2 = {}
    dict3 = {}
    day_list = []
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key1 in spend_necessary_sum_of_abs_month_day_average(userid, url).keys():
        if key1[4:6]in dict1 and key1[0:4]!=day_list[-1][0:4]:
            dict1[key1[4:6]] += 1
        else:
            dict1[key1[4:6]] = 1
    for key2,value2 in spend_necessary_sum_of_abs_month_day_average(userid, url).items():
        if key2[4:6] in dict2 and key2[0:4] != day_list[-1][0:4]:
            dict2[key2[4:6]] += value2
        elif key2[4:6] not in dict2 and key2[0:4] != day_list[-1][0:4]:
            dict2[key2[4:6]] = value2
    for key3, value3 in dict2.items():
        dict3[key3] = float(value3) / float(dict1[key3])
    return dict3
#每一相同月為key,每一相同月(不包含今年)之每日不必要總金額為value(兩層)(月->日)
def spend_unnecessary_sum_of_same_month_everyday(userid, url):
    dict={}
    day_list=[]
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key,value in spend_unnecessary_sum_of_abs_day(userid, url).items():
        if key[4:6] in dict and key[0:4]!=day_list[-1][0:4]:
            if key[6:] in dict[key[4:6]] :
                a=dict[key[4:6]][key[6:]]+value
                addtwodimdict(dict, key[4:6], key[6:], a)
                print(dict)
            elif key[6:] not in dict[key[4:6]]:
                addtwodimdict(dict, key[4:6], key[6:],value)
                print(dict)
        elif key[4:6] not in dict and key[0:4]!=day_list[-1][0:4]:
            addtwodimdict(dict, key[4:6], key[6:], value)
            print(dict)
    return dict
#每一相同月為key,每一相同月(不包含今年)之每日不必要總金額/次數為value(兩層)(月->日)
def spend_unnecessary_sum_of_same_month_everyday_average(userid, url):
    dict1={}
    dict2={}
    day_list = []
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key1 in spend_unnecessary_sum_of_abs_day(userid, url).keys():
        if key1[4:6] in dict1 and key1[0:4] != day_list[-1][0:4]:
            if key1[6:] in dict1[key1[4:6]]:
                a = dict1[key1[4:6]][key1[6:]] + 1
                addtwodimdict(dict1, key1[4:6], key1[6:], a)
                print(dict1)
            elif key1[6:] not in dict1[key1[4:6]]:
                addtwodimdict(dict1, key1[4:6], key1[6:], 1)
                print(dict1)
        elif key1[4:6] not in dict1 and key1[0:4] != day_list[-1][0:4]:
            addtwodimdict(dict1, key1[4:6], key1[6:], 1)
            print(dict1)
    for key2,value2 in spend_unnecessary_sum_of_same_month_everyday(userid, url).items():
        for key3, value3 in value2.items():
            b=float(value3)/float(dict1[key2][key3])
            addtwodimdict(dict2, key2, key3,b)
    return dict2
#每一相同月為key,每一相同月必須平均不必要金額(不包含今年)/次數為value
def spend_unnecessary_sum_of_same_month_day_average(userid, url):
    dict1 = {}
    dict2 = {}
    dict3 = {}
    day_list = []
    for i in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(i)
    for key1 in spend_unnecessary_sum_of_abs_month_day_average(userid, url).keys():
        if key1[4:6]in dict1 and key1[0:4]!=day_list[-1][0:4]:
            dict1[key1[4:6]] += 1
        else:
            dict1[key1[4:6]] = 1
    for key2,value2 in spend_unnecessary_sum_of_abs_month_day_average(userid, url).items():
        if key2[4:6] in dict2 and key2[0:4] != day_list[-1][0:4]:
            dict2[key2[4:6]] += value2
        elif key2[4:6] not in dict2 and key2[0:4] != day_list[-1][0:4]:
            dict2[key2[4:6]] = value2
    for key3, value3 in dict2.items():
        dict3[key3] = float(value3) / float(dict1[key3])
    return dict3

#去年與今年同月每日總花費比較折線圖
def current_previous_same_month_day_Line_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    #fig.subplots_adjust(top=0.8)
    day_list=[]
    current_sum_list=[]
    previous_sum_list=[]
    previous_average_list=[]
    num_dict1 = {}
    num_dict2 = {}
    num_dict3 = {}
    p = 0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    if day_list[4:6] == '1' or '3' or '5' or '7' or '8' or '10' or '12':
        p = 31
    elif day_list[4:6] == '4' or '6' or '9' or '11':
        p = 30
    elif day_list[4:6] == '2':
        p = 29
    for i in range(1, p + 1):
        num_dict1[i] = 0
        num_dict2[i] = 0
        num_dict3[i] = 0
    for key2, value2 in spend_sum_of_abs_day(userid, url).items():
        for key3, value3 in num_dict1.items():
            if key2[0:6] == day_list[-1][0:6]:
                if int(key2[6:]) == key3:
                    num_dict1[key3] = value2
        for key4, value4 in num_dict2.items():
            if int(key2[0:4]) == int(day_list[-1][0:4]) - 1 and key2[4:6] == day_list[-1][4:6]:
                if int(key2[6:]) == key4:
                    num_dict2[key4] = value2
    for key5, value5 in num_dict1.items():
        current_sum_list.append(value5)
    for key6, value6 in num_dict2.items():
        previous_sum_list.append(value6)
    # print(current_sum_list)
    # print(previous_sum_list)
    # print(len(current_sum_list))
    # print(len(previous_sum_list))
    for key7, value7 in spend_sum_of_same_month_everyday_average(userid, url)[day_list[-1][4:6]].items():
        for key8, value8 in num_dict3.items():
            if int(key7) == key8:
                num_dict3[key8] = value7
    for key9, value9 in num_dict3.items():
        previous_average_list.append(value9)
    #if  day_list[-1][4:6]==1 or 3 or 5 or 7 or 8 or 10 or 12:
    plt.bar(range(1, len(previous_sum_list) + 1), previous_average_list, color='#C0C0C0',label='{}月之往年每日平均'.format(day_list[-1][4:6]))
    #plt.legend(loc='upper right')
    #plt.twinx()
    plt.plot(range(1, len(previous_sum_list) + 1), previous_sum_list, color='#000080', label="{}年{}月".format(str(int(day_list[-1][0:4])-1),day_list[-1][4:6]),marker='o')
    plt.plot(range(1, len(previous_sum_list) + 1), current_sum_list, color='#FF8C00',label="{}年{}月".format(day_list[-1][0:4], day_list[-1][4:6]), marker='o')
    plt.axhline(spend_sum_of_same_month_day_average(userid, url)[day_list[-1][4:6]], color='r',label='{}月之往年平均{}元'.format(day_list[-1][4:6],int(spend_sum_of_same_month_day_average(userid, url)[day_list[-1][4:6]])))
    plt.legend(loc='upper left',fontsize=10)
    plt.xlim(0,len(previous_sum_list)+1)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(50))
    plt.xlabel('日期', fontdict={ 'color': 'k', 'size': 12})
    plt.ylabel('金額', fontdict={ 'color': 'k', 'size': 12})
    ax.set_title('今年與往年同月每日平均金額比較圖', fontdict={ 'color': 'k', 'size': 15}, pad=10)
    plt.grid(b=True, axis='y')
    filename = userid + "1.png"
    plt.savefig(filename)
#去年與今年同月每日必要總花費比較折線圖
def current_previous_necessary_same_month_day_Line_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    # fig.subplots_adjust(top=0.8)
    day_list = []
    current_sum_list = []
    previous_sum_list = []
    previous_average_list = []
    num_dict1={}
    num_dict2 = {}
    num_dict3 = {}
    p=0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    if day_list[4:6]=='1' or '3' or '5' or '7' or '8' or '10' or '12':
        p=31
    elif day_list[4:6]=='4' or '6' or '9' or '11' :
        p=30
    elif day_list[4:6]=='2' :
        p=29
    for i in range(1,p+1):
        num_dict1[i]=0
        num_dict2[i]=0
        num_dict3[i] = 0
    for key2, value2 in spend_necessary_sum_of_abs_day(userid, url).items():
        for key3, value3 in num_dict1.items():
            if key2[0:6] == day_list[-1][0:6]:
                if int(key2[6:])==key3:
                    num_dict1[key3]=value2
        for key4, value4 in num_dict2.items():
            if int(key2[0:4]) == int(day_list[-1][0:4])-1 and key2[4:6] == day_list[-1][4:6]:
                if int(key2[6:]) == key4:
                    num_dict2[key4] =value2
    for key5, value5 in num_dict1.items():
        current_sum_list.append(value5)
    for key6, value6 in num_dict2.items():
        previous_sum_list.append(value6)
    #print(current_sum_list)
    #print(previous_sum_list)
    #print(len(current_sum_list))
    #print(len(previous_sum_list))
    for key7,value7 in spend_necessary_sum_of_same_month_everyday_average(userid, url)[day_list[-1][4:6]].items():
        for key8, value8 in num_dict3.items():
            if int(key7)==key8:
                num_dict3[key8]=value7
    for key9, value9 in num_dict3.items():
        previous_average_list.append(value9)
    # if  day_list[-1][4:6]==1 or 3 or 5 or 7 or 8 or 10 or 12:
    plt.bar(range(1, len(previous_sum_list) + 1), previous_average_list, color='#C0C0C0',label='{}月之往年每日平均'.format(day_list[-1][4:6]))
    # plt.legend(loc='upper right')
    # plt.twinx()
    plt.plot(range(1, len(previous_sum_list) + 1), previous_sum_list, color='#000080',label="{}年{}月".format(str(int(day_list[-1][0:4]) - 1), day_list[-1][4:6]), marker='o')
    plt.plot(range(1, len(previous_sum_list) + 1), current_sum_list, color='#FF8C00',label="{}年{}月".format(day_list[-1][0:4], day_list[-1][4:6]), marker='o')
    plt.axhline(spend_necessary_sum_of_same_month_day_average(userid, url)[day_list[-1][4:6]], color='r',label='{}月之往年平均{}元'.format(day_list[-1][4:6],int(spend_necessary_sum_of_same_month_day_average(userid, url)[day_list[-1][4:6]])))
    plt.legend(loc='upper left', fontsize=10)
    plt.xlim(0, len(previous_sum_list) + 1)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(50))
    plt.xlabel('日期', fontdict={ 'color': 'k', 'size': 12})
    plt.ylabel('金額', fontdict={'color': 'k', 'size': 12})
    ax.set_title('今年與往年同月每日平均必要金額比較圖', fontdict={ 'color': 'k', 'size': 15}, pad=10)
    plt.grid(b=True, axis='y')
    filename = userid + "2.png"
    plt.savefig(filename)
#去年與今年同月每日必要總花費比較折線圖
def current_previous_unnecessary_same_month_day_Line_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    # fig.subplots_adjust(top=0.8)
    day_list = []
    current_sum_list = []
    previous_sum_list = []
    previous_average_list = []
    num_dict1={}
    num_dict2 = {}
    num_dict3 = {}
    p=0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    if day_list[4:6]=='1' or '3' or '5' or '7' or '8' or '10' or '12':
        p=31
    elif day_list[4:6]=='4' or '6' or '9' or '11' :
        p=30
    elif day_list[4:6]=='2' :
        p=29
    for i in range(1,p+1):
        num_dict1[i]=0
        num_dict2[i]=0
        num_dict3[i] = 0
    for key2, value2 in spend_unnecessary_sum_of_abs_day(userid, url).items():
        for key3, value3 in num_dict1.items():
            if key2[0:6] == day_list[-1][0:6]:
                if int(key2[6:])==key3:
                    num_dict1[key3]=value2
        for key4, value4 in num_dict2.items():
            if int(key2[0:4]) == int(day_list[-1][0:4])-1 and key2[4:6] == day_list[-1][4:6]:
                if int(key2[6:]) == key4:
                    num_dict2[key4] =value2
    for key5, value5 in num_dict1.items():
        current_sum_list.append(value5)
    for key6, value6 in num_dict2.items():
        previous_sum_list.append(value6)
    #print(current_sum_list)
    #print(previous_sum_list)
    #print(len(current_sum_list))
    #print(len(previous_sum_list))
    for key7,value7 in spend_unnecessary_sum_of_same_month_everyday_average(userid, url)[day_list[-1][4:6]].items():
        for key8, value8 in num_dict3.items():
            if int(key7)==key8:
                num_dict3[key8]=value7
    for key9, value9 in num_dict3.items():
        previous_average_list.append(value9)
    # if  day_list[-1][4:6]==1 or 3 or 5 or 7 or 8 or 10 or 12:
    plt.bar(range(1, len(previous_sum_list) + 1), previous_average_list, color='#C0C0C0',label='{}月之往年每日平均'.format(day_list[-1][4:6]))
    # plt.legend(loc='upper right')
    # plt.twinx()
    plt.plot(range(1, len(previous_sum_list) + 1), previous_sum_list, color='#000080',label="{}年{}月".format(str(int(day_list[-1][0:4]) - 1), day_list[-1][4:6]), marker='o')
    plt.plot(range(1, len(previous_sum_list) + 1), current_sum_list, color='#FF8C00',label="{}年{}月".format(day_list[-1][0:4], day_list[-1][4:6]), marker='o')
    plt.axhline(spend_unnecessary_sum_of_same_month_day_average(userid, url)[day_list[-1][4:6]], color='r',label='{}月之往年平均{}元'.format(day_list[-1][4:6],int(spend_unnecessary_sum_of_same_month_day_average(userid, url)[day_list[-1][4:6]])))
    plt.legend(loc='upper left', fontsize=10)
    plt.xlim(0, len(previous_sum_list) + 1)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(50))
    plt.xlabel('日期', fontdict={ 'color': 'k', 'size': 12})
    plt.ylabel('金額', fontdict={ 'color': 'k', 'size': 12})
    ax.set_title('今年與往年同月每日平均不必要金額比較圖', fontdict={ 'color': 'k', 'size': 15}, pad=10)
    plt.grid(b=True, axis='y')
    filename = userid + "3.png"
    plt.savefig(filename)
#當月必要與不必要總花費占比圓餅圖
def current_month_necessary_and_unnecessary_Pie_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    day_list = []
    necessary_unnecessary_list=[]
    necessarity_list=['必要','不必要']
    necessary_sum=0
    unnecessary_sum=0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    for key2,value2 in spend_necessary_sum_of_abs_day(userid, url).items():
        if key2[0:6]==day_list[-1][0:6]:
            necessary_sum+=value2
    for key3, value3 in spend_unnecessary_sum_of_abs_day(userid, url).items():
        if key3[0:6] == day_list[-1][0:6]:
            unnecessary_sum += value3

    def func(pct, allvals):
        if "{:.1f}%".format(pct)=="{:.1f}%".format((float(necessary_sum)/float(necessary_sum+unnecessary_sum))*100):
            absolute=allvals[0]
        else:
            absolute=allvals[1]
        return "{:.1f}%\n({:d} 元)".format(pct, absolute)
    necessary_unnecessary_list.append(necessary_sum)
    necessary_unnecessary_list.append(unnecessary_sum)
    ax.pie(necessary_unnecessary_list, textprops={ 'color': 'k', 'size': 18}, autopct=lambda pct: func(pct, necessary_unnecessary_list),startangle=90,colors=['#87e8e8','#f5b5c6'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.legend( necessarity_list,title="必要性", fontsize=10,loc="center left",bbox_to_anchor=(-0.1,0, 0, 1))
    ax.set_title("當月必要與不必要總花費占比", fontsize=15)
    filename = userid + "4.png"
    plt.savefig(filename)
#當月必要與不必要總花費占比與去年比較之圓餅圖
def current_month_necessary_and_unnecessary_double_Pie_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig,ax = plt.subplots(1,2)
    #fig = plt.figure(constrained_layout=True)
    day_list = []
    necessary_unnecessary_list1 = []
    necessary_unnecessary_list2=[]
    necessarity_list=['必要','不必要']
    necessary_sum1= 0
    unnecessary_sum1= 0
    necessary_sum2=0
    unnecessary_sum2=0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    for key2,value2 in spend_necessary_sum_of_abs_day(userid, url).items():
        if key2[0:6]==day_list[-1][0:6]:
            necessary_sum2+=value2
    for key3, value3 in spend_unnecessary_sum_of_abs_day(userid, url).items():
        if key3[0:6] == day_list[-1][0:6]:
            unnecessary_sum2 += value3
    for key4,value4 in spend_necessary_sum_of_abs_month(userid, url).items():
        if key4[4:6]==day_list[-1][4:6] and int(key4[0:4]) == int(day_list[-1][0:4])-1:
            necessary_sum1+=value4
    for key5, value5 in spend_unnecessary_sum_of_abs_month(userid, url).items():
        if key5[4:6] == day_list[-1][4:6] and int(key5[0:4]) == int(day_list[-1][0:4])-1:
            unnecessary_sum1 += value5


    def func(necessary_sum,unnecessary_sum,pct,allvals):
        if "{:.1f}%".format(pct)=="{:.1f}%".format((float(necessary_sum)/float(necessary_sum+unnecessary_sum))*100):
            absolute=allvals[0]
        else:
            absolute=allvals[1]
        return "{:.1f}%\n({:d} 元)".format(pct, absolute)
    necessary_unnecessary_list1.append(necessary_sum1)
    necessary_unnecessary_list1.append(unnecessary_sum1)
    ax[0].pie(necessary_unnecessary_list1, textprops={ 'color': 'k', 'size': 15},autopct=lambda pct: func(necessary_sum1, unnecessary_sum1, pct,necessary_unnecessary_list1), startangle=90,colors=['#87e8e8','#f5b5c6'])
    ax[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax[0].legend(necessarity_list, title="必要性", fontsize=11, loc="center left",bbox_to_anchor=(-0.3, -0.5, 0, 1))
    ax[0].set_title("去年當月必要與不必要總花費占比", fontsize=12,pad=-10)
    necessary_unnecessary_list2.append(necessary_sum2)
    necessary_unnecessary_list2.append(unnecessary_sum2)
    ax[1].pie(necessary_unnecessary_list2, textprops={ 'color': 'k', 'size': 15}, autopct=lambda pct: func(necessary_sum2,unnecessary_sum2,pct, necessary_unnecessary_list2),startangle=90,colors=['#87e8e8','#f5b5c6'])
    ax[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #ax_dict["this year"].legend( necessarity_list,title="必要性", fontsize=10,loc="center left",bbox_to_anchor=(-0.1,0, 0, 1))
    ax[1].set_title("今年當月必要與不必要總花費占比", fontsize=12,pad=-10)

    #identify_axes(ax_dict)
    filename = userid + "5.png"
    plt.savefig(filename)
#當月各項總花費占比圓餅圖
def current_month_item_Pie_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    day_list = []
    item_list=[]
    item_list_d=[]
    item_name_list=['飲食','生活用品','娛樂','學業','交通']
    food_sum=0
    daily_necessities_sum=0
    entertainment_sum=0
    academic_sum = 0
    traffic_sum=0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    for key2, value2 in spend_item_sum_of_abs_month(userid, url).items():
        if key2[0:6] == day_list[-1][0:6]:
            if '飲食' in value2:
                food_sum += value2['飲食']
            if '生活用品' in value2:
                daily_necessities_sum+= value2['生活用品']
            if '娛樂' in value2:
                entertainment_sum += value2['娛樂']
            if '學業' in value2:
                academic_sum += value2['學業']
            if '交通' in value2:
                traffic_sum += value2['交通']
    """
    def func(pct, allvals):
        if "{:.1f}%".format(pct)=="{:.1f}%".format((float(food_sum)/float(sum(item_list)))*100):
            absolute=allvals[0]
        elif "{:.1f}%".format(pct)=="{:.1f}%".format((float(daily_necessities_sum)/float(sum(item_list)))*100):
            absolute=allvals[1]
        elif "{:.1f}%".format(pct)=="{:.1f}%".format((float(entertainment_sum)/float(sum(item_list)))*100):
            absolute=allvals[2]
        elif "{:.1f}%".format(pct)=="{:.1f}%".format((float(academic_sum)/float(sum(item_list)))*100):
            absolute=allvals[3]
        elif "{:.1f}%".format(pct)=="{:.1f}%".format((float(traffic_sum)/float(sum(item_list)))*100):
            absolute=allvals[4]
        return "{:.1f}%\n({:d} 元)".format(pct, absolute)
    """
    item_list.append(food_sum)
    item_list.append(daily_necessities_sum)
    item_list.append(entertainment_sum)
    item_list.append(academic_sum)
    item_list.append(traffic_sum)
    for i in item_list:
        item_list_d.append(str(i)+'元')
    ax.pie(item_list, textprops={ 'color': 'k', 'size': 15}, autopct='%1.1f%%',startangle=90,colors=['#FF8C00','#6495ED','#f26682','#48D1CC', '#BC8F8F'], labels = item_list_d)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.legend(item_name_list, title="項目", fontsize=10,  loc="center left",bbox_to_anchor=(-0.15,-0.4, 0, 1))
    ax.set_title("當月各項總花費占比", fontsize=15, pad=15)
    filename = userid + "6.png"
    plt.savefig(filename)
#當月各項總花費占比與去年比較之圓餅圖
def current_month_item_double_Pie_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(1,2)
    #fig = plt.figure(constrained_layout=True)
    day_list = []
    item_list1 = []
    item_list2 = []
    item_list_d1 = []
    item_list_d2 = []
    item_name_list = ['飲食', '生活用品', '娛樂', '學業', '交通']
    food_sum1 = 0
    daily_necessities_sum1 = 0
    entertainment_sum1 = 0
    academic_sum1 = 0
    traffic_sum1 = 0
    food_sum2 = 0
    daily_necessities_sum2 = 0
    entertainment_sum2 = 0
    academic_sum2 = 0
    traffic_sum2 = 0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    for key2, value2 in spend_item_sum_of_abs_month(userid, url).items():
        if key2[0:6] == day_list[-1][0:6]:
            if '飲食' in value2:
                food_sum2 += value2['飲食']
            if '生活用品' in value2:
                daily_necessities_sum2 += value2['生活用品']
            if '娛樂' in value2:
                entertainment_sum2 += value2['娛樂']
            if '學業' in value2:
                academic_sum2 += value2['學業']
            if '交通' in value2:
                traffic_sum2 += value2['交通']
    for key3, value3 in spend_item_sum_of_abs_month(userid, url).items():
        if key3[4:6]==day_list[-1][4:6] and int(key3[0:4]) == int(day_list[-1][0:4])-1:
            if '飲食' in value3:
                food_sum1 += value3['飲食']
            if '生活用品' in value3:
                daily_necessities_sum1 += value3['生活用品']
            if '娛樂' in value3:
                entertainment_sum1 += value3['娛樂']
            if '學業' in value3:
                academic_sum1 += value3['學業']
            if '交通' in value3:
                traffic_sum1 += value3['交通']
    item_list1.append(food_sum1)
    item_list1.append(daily_necessities_sum1)
    item_list1.append(entertainment_sum1)
    item_list1.append(academic_sum1)
    item_list1.append(traffic_sum1)
    for i in item_list1:
        item_list_d1.append(str(i) + '元')
    item_list2.append(food_sum2)
    item_list2.append(daily_necessities_sum2)
    item_list2.append(entertainment_sum2)
    item_list2.append(academic_sum2)
    item_list2.append(traffic_sum2)
    for i in item_list2:
        item_list_d2.append(str(i) + '元')
    """
    ax_dict = fig.subplot_mosaic(
        [
            ["last year", "this year"],
        ],
    )
    """
    ax[0].pie(item_list1, textprops={ 'color': 'k', 'size': 12}, autopct='%1.1f%%', startangle=90,colors=['#FF8C00', '#6495ED', '#DC143C', '#48D1CC', '#BC8F8F'], labels=item_list_d1)
    ax[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax[0].legend(item_name_list, title="項目", fontsize=10, loc="center left", bbox_to_anchor=(-0.3, -0.4, 0, 1))
    ax[0].set_title("去年當月各項總花費占比", fontsize=15, pad=-10)
    ax[1].pie(item_list2, textprops={ 'color': 'k', 'size': 12}, autopct='%1.1f%%', startangle=90,colors=['#FF8C00', '#6495ED', '#DC143C', '#48D1CC', '#BC8F8F'], labels=item_list_d2)
    ax[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #ax.legend(item_name_list, title="項目", fontsize=10, loc="center left", bbox_to_anchor=(-0.15, -0.4, 0, 1))
    ax[1].set_title("今年當月各項總花費占比", fontsize=15, pad=-10)
    #identify_axes(ax_dict)
    filename = userid + "7.png"
    plt.savefig(filename)
#當月各項必要性總花費長條圖
def current_month_necessary_and_unnecessary_item_Bar_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    day_list = []
    item_necessary_list = []
    item_unnecessary_list = []
    item_list=[]
    item_name_list=['飲食','生活用品','娛樂','學業','交通']
    food_necessary_sum = 0
    daily_necessities_necessary_sum = 0
    entertainment_necessary_sum = 0
    academic_necessary_sum = 0
    traffic_necessary_sum = 0
    food_unnecessary_sum = 0
    daily_necessities_unnecessary_sum = 0
    entertainment_unnecessary_sum = 0
    academic_unnecessary_sum = 0
    traffic_unnecessary_sum = 0
    food_sum=0
    daily_necessities_sum=0
    entertainment_sum=0
    academic_sum = 0
    traffic_sum=0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    for key2, value2 in spend_item_sum_of_abs_month(userid, url).items():
        if key2[0:6] == day_list[-1][0:6]:
            if '飲食' in value2:
                food_sum += value2['飲食']
            if '生活用品' in value2:
                daily_necessities_sum += value2['生活用品']
            if '娛樂' in value2:
                entertainment_sum += value2['娛樂']
            if '學業' in value2:
                academic_sum += value2['學業']
            if '交通' in value2:
                traffic_sum += value2['交通']
    item_list.append(food_sum)
    item_list.append(daily_necessities_sum)
    item_list.append(entertainment_sum)
    item_list.append(academic_sum)
    item_list.append(traffic_sum)
    for key3,value3 in spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url).items():
        for key4, value4 in value3.items():
            if key3[0:6] == day_list[-1][0:6]:
                if '必要'==key4:
                    if '飲食' in value4:
                        food_necessary_sum += value4['飲食']
                    if '生活用品' in value4:
                        daily_necessities_necessary_sum += value4['生活用品']
                    if '娛樂' in value4:
                        entertainment_necessary_sum += value4['娛樂']
                    if '學業' in value4:
                        academic_necessary_sum += value4['學業']
                    if '交通' in value4:
                        traffic_necessary_sum += value4['交通']
                if '不必要'==key4:
                    if '飲食' in value4:
                        food_unnecessary_sum += value4['飲食']
                    if '生活用品' in value4:
                        daily_necessities_unnecessary_sum += value4['生活用品']
                    if '娛樂' in value4:
                        entertainment_unnecessary_sum += value4['娛樂']
                    if '學業' in value4:
                        academic_unnecessary_sum += value4['學業']
                    if '交通' in value4:
                        traffic_unnecessary_sum += value4['交通']
    item_necessary_list.append(food_necessary_sum)
    item_necessary_list.append(daily_necessities_necessary_sum)
    item_necessary_list.append(entertainment_necessary_sum)
    item_necessary_list.append(academic_necessary_sum)
    item_necessary_list.append(traffic_necessary_sum)
    item_unnecessary_list.append(food_unnecessary_sum)
    item_unnecessary_list.append(daily_necessities_unnecessary_sum)
    item_unnecessary_list.append(entertainment_unnecessary_sum)
    item_unnecessary_list.append(academic_unnecessary_sum)
    item_unnecessary_list.append(traffic_unnecessary_sum)

    col_count = 5
    bar_width = 0.2
    index = np.arange(col_count)
    item_necessary_list=np.array(item_necessary_list)
    item_unnecessary_list = np.array(item_unnecessary_list)
    item_list= np.array(item_list)
    item_name_list= np.array(item_name_list)

    necessary = plt.bar(index,item_necessary_list,bar_width,alpha=.4,label="必要")
    unnecessary = plt.bar(index + 0.3,item_unnecessary_list,bar_width,alpha=.4,label="不必要")
    sum= plt.bar(index + 0.6,item_list,bar_width,alpha=.4,label="總數")  # x,y ,width

    def createLabels(data):
        for item in data:
            height = item.get_height()
            plt.text(item.get_x() + item.get_width() / 2.,height * 1.05,'%d' % int(height),ha="center",va="bottom")

    createLabels(necessary)
    createLabels(unnecessary)
    createLabels(sum)

    plt.ylabel("金額", fontdict={'color': 'k', 'size': 12})
    plt.xlabel("項目", fontdict={ 'color': 'k', 'size': 12})
    plt.title("當月各項必要性總花費", fontdict={ 'color': 'k', 'size': 15}, pad=16)
    plt.xticks(index + .6 / 2, item_name_list)
    plt.legend()
    plt.grid(b=True, axis='y')
    filename = userid + "8.png"
    plt.savefig(filename)
#去年與今年當月各項必要性總花費長條圖
def current_month_necessary_and_unnecessary_item_comparison_Bar_Chart(userid, url):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(25, 10))
    day_list = []
    item_necessary_list1 = []
    item_unnecessary_list1 = []
    item_necessary_list2 = []
    item_unnecessary_list2 = []
    item_list1=[]
    item_list2 = []
    item_name_list=['飲食','生活用品','娛樂','學業','交通']
    food_necessary_sum1 = 0
    daily_necessities_necessary_sum1 = 0
    entertainment_necessary_sum1 = 0
    academic_necessary_sum1 = 0
    traffic_necessary_sum1 = 0
    food_unnecessary_sum1 = 0
    daily_necessities_unnecessary_sum1 = 0
    entertainment_unnecessary_sum1 = 0
    academic_unnecessary_sum1 = 0
    traffic_unnecessary_sum1 = 0
    food_sum1=0
    daily_necessities_sum1=0
    entertainment_sum1=0
    academic_sum1 = 0
    traffic_sum1=0
    food_necessary_sum2 = 0
    daily_necessities_necessary_sum2 = 0
    entertainment_necessary_sum2 = 0
    academic_necessary_sum2 = 0
    traffic_necessary_sum2= 0
    food_unnecessary_sum2 = 0
    daily_necessities_unnecessary_sum2 = 0
    entertainment_unnecessary_sum2 = 0
    academic_unnecessary_sum2= 0
    traffic_unnecessary_sum2= 0
    food_sum2= 0
    daily_necessities_sum2= 0
    entertainment_sum2= 0
    academic_sum2= 0
    traffic_sum2= 0
    for key1 in spend_sum_of_abs_day(userid, url).keys():
        day_list.append(key1)
    for key2, value2 in spend_item_sum_of_abs_month(userid, url).items():
        if key2[0:6] == day_list[-1][0:6]:
            if '飲食' in value2:
                food_sum2 += value2['飲食']
            if '生活用品' in value2:
                daily_necessities_sum2 += value2['生活用品']
            if '娛樂' in value2:
                entertainment_sum2 += value2['娛樂']
            if '學業' in value2:
                academic_sum2 += value2['學業']
            if '交通' in value2:
                traffic_sum2 += value2['交通']
    item_list2.append(food_sum2)
    item_list2.append(daily_necessities_sum2)
    item_list2.append(entertainment_sum2)
    item_list2.append(academic_sum2)
    item_list2.append(traffic_sum2)
    for key3,value3 in spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url).items():
        for key4, value4 in value3.items():
            if key3[0:6] == day_list[-1][0:6]:
                if '必要'==key4:
                    if '飲食' in value4:
                        food_necessary_sum2 += value4['飲食']
                    if '生活用品' in value4:
                        daily_necessities_necessary_sum2 += value4['生活用品']
                    if '娛樂' in value4:
                        entertainment_necessary_sum2 += value4['娛樂']
                    if '學業' in value4:
                        academic_necessary_sum2 += value4['學業']
                    if '交通' in value4:
                        traffic_necessary_sum2 += value4['交通']
                if '不必要'==key4:
                    if '飲食' in value4:
                        food_unnecessary_sum2 += value4['飲食']
                    if '生活用品' in value4:
                        daily_necessities_unnecessary_sum2 += value4['生活用品']
                    if '娛樂' in value4:
                        entertainment_unnecessary_sum2 += value4['娛樂']
                    if '學業' in value4:
                        academic_unnecessary_sum2 += value4['學業']
                    if '交通' in value4:
                        traffic_unnecessary_sum2 += value4['交通']
    item_necessary_list2.append(food_necessary_sum2)
    item_necessary_list2.append(daily_necessities_necessary_sum2)
    item_necessary_list2.append(entertainment_necessary_sum2)
    item_necessary_list2.append(academic_necessary_sum2)
    item_necessary_list2.append(traffic_necessary_sum2)
    item_unnecessary_list2.append(food_unnecessary_sum2)
    item_unnecessary_list2.append(daily_necessities_unnecessary_sum2)
    item_unnecessary_list2.append(entertainment_unnecessary_sum2)
    item_unnecessary_list2.append(academic_unnecessary_sum2)
    item_unnecessary_list2.append(traffic_unnecessary_sum2)

    for key5, value5 in spend_item_sum_of_abs_month(userid, url).items():
        if key5[4:6] == day_list[-1][4:6] and int(key5[0:4]) == int(day_list[-1][0:4])-1:
            if '飲食' in value5:
                food_sum1 += value5['飲食']
            if '生活用品' in value5:
                daily_necessities_sum1 += value5['生活用品']
            if '娛樂' in value5:
                entertainment_sum1 += value5['娛樂']
            if '學業' in value5:
                academic_sum1 += value5['學業']
            if '交通' in value5:
                traffic_sum1 += value5['交通']
    item_list1.append(food_sum1)
    item_list1.append(daily_necessities_sum1)
    item_list1.append(entertainment_sum1)
    item_list1.append(academic_sum1)
    item_list1.append(traffic_sum1)
    for key6,value6 in spend_necessary_and_unnecessary_item_sum_of_abs_month(userid, url).items():
        for key7, value7 in value6.items():
            if key6[4:6] == day_list[-1][4:6] and int(key6[0:4]) == int(day_list[-1][0:4])-1:
                if '必要'==key7:
                    if '飲食' in value7:
                        food_necessary_sum1 += value7['飲食']
                    if '生活用品' in value7:
                        daily_necessities_necessary_sum1 += value7['生活用品']
                    if '娛樂' in value7:
                        entertainment_necessary_sum1 += value7['娛樂']
                    if '學業' in value7:
                        academic_necessary_sum1 += value7['學業']
                    if '交通' in value7:
                        traffic_necessary_sum1 += value7['交通']
                if '不必要'==key7:
                    if '飲食' in value7:
                        food_unnecessary_sum1 += value7['飲食']
                    if '生活用品' in value7:
                        daily_necessities_unnecessary_sum1 += value7['生活用品']
                    if '娛樂' in value7:
                        entertainment_unnecessary_sum1 += value7['娛樂']
                    if '學業' in value7:
                        academic_unnecessary_sum1 += value7['學業']
                    if '交通' in value7:
                        traffic_unnecessary_sum1 += value7['交通']
    item_necessary_list1.append(food_necessary_sum1)
    item_necessary_list1.append(daily_necessities_necessary_sum1)
    item_necessary_list1.append(entertainment_necessary_sum1)
    item_necessary_list1.append(academic_necessary_sum1)
    item_necessary_list1.append(traffic_necessary_sum1)
    item_unnecessary_list1.append(food_unnecessary_sum1)
    item_unnecessary_list1.append(daily_necessities_unnecessary_sum1)
    item_unnecessary_list1.append(entertainment_unnecessary_sum1)
    item_unnecessary_list1.append(academic_unnecessary_sum1)
    item_unnecessary_list1.append(traffic_unnecessary_sum1)

    col_count = 5
    bar_width = 0.1
    index = np.arange(col_count)
    item_name_list = np.array(item_name_list)

    item_necessary_list1 = np.array(item_necessary_list1)
    item_unnecessary_list1 = np.array(item_unnecessary_list1)
    item_list1 = np.array(item_list1)
    item_necessary_list2 = np.array(item_necessary_list2)
    item_unnecessary_list2 = np.array(item_unnecessary_list2)
    item_list2 = np.array(item_list2)


    necessary1 = plt.bar(index, item_necessary_list1, bar_width, alpha=.4, label="{}年必要".format(str(int(day_list[-1][0:4])-1)),color='#191970')
    necessary2 = plt.bar(index+0.108, item_necessary_list2, bar_width, alpha=.4, label="{}年必要".format(day_list[-1][0:4]),color='#6495ED')
    unnecessary1 = plt.bar(index+0.258 , item_unnecessary_list1, bar_width, alpha=.4, label="{}年不必要".format(str(int(day_list[-1][0:4])-1)),color='#8B0000')
    unnecessary2 = plt.bar(index +0.366, item_unnecessary_list2, bar_width, alpha=.4,label="{}年不必要".format(day_list[-1][0:4]),color='#F08080')
    sum1 = plt.bar(index+0.516 , item_list1, bar_width, alpha=.4, label="{}年總數".format(str(int(day_list[-1][0:4])-1)),color='#556B2F')  # x,y ,width
    sum2 = plt.bar(index +0.624, item_list2, bar_width, alpha=.4, label="{}年總數".format(day_list[-1][0:4]),color='#9ACD32')  # x,y ,width

    def createLabels(data):
        for item in data:
            height = item.get_height()
            plt.text(item.get_x() + item.get_width() / 2.,height * 1.05,'%d' % int(height),ha="center",va="bottom")

    createLabels(necessary1)
    createLabels(necessary2)
    createLabels(unnecessary1)
    createLabels(unnecessary2)
    createLabels(sum1)
    createLabels(sum2)

    plt.ylabel("金額", fontdict={'color': 'k', 'size': 15})
    plt.xlabel("項目", fontdict={'color': 'k', 'size': 15})
    plt.title("去年與今年當月各項必要性總花費", fontdict={'color': 'k', 'size': 18}, pad=20)
    plt.xticks(index + .6 / 2, item_name_list,fontsize=15)
    plt.legend(fontsize=13)
    plt.grid(b=True, axis='y')
    filename = userid + "9.png"
    plt.savefig(filename)

#if __name__ == '__main__':
        #print(get_spend_csv())
        #print(get_all_user_id_list_from_spend_csv_url('https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
        #print(get_all_user_id_list_from_income_csv_url('https://docs.google.com/spreadsheets/d/1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4/export?format=csv'))
        #print(creat_user_csv_data('U0a84d6de855ff90af62127932c7fde1f', '123'))
    #data = get_user_data_from_spend_csv_url('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv')
    #print(data)
        #print(creat_user_csv_data('U0a84d6de855ff90af62127932c7fde1f', data))
        #print(creat_all_user_spend_csv_data('https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
        #print(get_user_data_from_spend_csv_url('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_abs_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_abs_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_abs_year_month_average('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_abs_year_day_average('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_abs_month_day_average('U0a84d6de855ff90af62127932c7fde1f', 'https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_abs_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_abs_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_abs_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_abs_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_abs_year('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_abs_year('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_abs_year_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_abs_year_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_abs_year_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_abs_year_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_abs_month_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_abs_month_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_abs_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_abs_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_abs_year('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_abs_year_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_abs_year_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_abs_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_abs_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_abs_year('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_abs_year_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_abs_year_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_abs_month_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_same_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_same_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_same_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_unnecessary_sum_of_same_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_same_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_same_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_same_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_item_sum_of_same_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_same_day('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_same_month('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_same_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_and_unnecessary_item_sum_of_same_month_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_month_everyday('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_month_everyday_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_sum_of_same_month_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_month_everyday('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_month_everyday_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(spend_necessary_sum_of_same_month_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    # print(spend_unnecessary_sum_of_same_month_everyday('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    # print(spend_unnecessary_sum_of_same_month_everyday_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    # print(spend_unnecessary_sum_of_same_month_day_average('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))

    #print(current_previous_same_month_day_Line_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_previous_necessary_same_month_day_Line_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_previous_unnecessary_same_month_day_Line_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_month_necessary_and_unnecessary_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_month_necessary_and_unnecessary_double_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_month_item_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_month_item_double_Pie_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_month_necessary_and_unnecessary_item_Bar_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
    #print(current_month_necessary_and_unnecessary_item_comparison_Bar_Chart('U0a84d6de855ff90af62127932c7fde1f','https://docs.google.com/spreadsheets/d/1-ierB_MQoeLlcOvHocc3NWeJCp2p8FQYzt5TVsMFfvY/export?format=csv'))
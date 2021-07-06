# Linebot-project

## Table of contents
* [About The Project](#about-the-project)
* [Technologies](#technologies)
* [Getting Started](#getting-started)
* [Getting Started with docker](#getting-started-with-docker)
* [Check](#check)

## About The Project
The goal of this project is to build an APP to help university students reduce their unnecessary living expenses.

Here's the function of APP :
* Chart function : Show the comparison of before and future's living expenses, percentage of monthly expenses, etc.
* Price comparison function : Compare different price on different online shop.
* Reminder function : When users did not track their expenses in two days, the reminder will notice users in next day.
* Consume analyze function: Compare each term of expenses of users with university students.
* Balance inquiry function : Until the end of a month, show the average amount of money which can be used per day. 
* Modify data function: Able to revise the numbers that users had already input.
* Expenses inquiry function : Search for the Xth expenses, the expenses of today, etc.

## Technologies
Project is created with :
* Python version : 3.9.2
* Django version : latest

## Getting Started
This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.

### Prerequisites
```
$ pip install django
$ pip install line-bot-sdk
```
* Git clone this project.
* Create a linebot account 
1. Copy the **channel secret** and **channel access token** of your account's basic setting to a notebook. They will be used later.
2. Go to '回應設定' in your LINE Official Account Manager, close '自動回應訊息' and open 'Webhook'.

<img src="https://i.imgur.com/CdcdXuu.jpg" width="40%"/> <img src="https://i.imgur.com/Szh55m5.jpg" width="40%"/>

* Ngrok
1. Sign up for [ngrok](https://ngrok.com/) and download file which is coressponding to your computer's version.  
2. Unzip the file and enter `$ ngrok authtoken <your authtoken>` and `$ ngrok http 8000`
![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_e4f71cf1b9cde8300de6b8db6919663d.png)
3. Copy the link generate by ngrok to Webhook URL in Line Messaging API and add `/callback`.
4. Open Use webhook
![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_d266b21c2251bbcaf372b6c18742e492.png)

### Installation
1. Open the terminal and enter :

```
$ pip install matplotlib
$ pip install pandas
$ pip install numpy
$ pip install dateutil
$ pip install apscheduler
$ pip install gspread
$ pip install --upgrade oauth2client
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
$ pip install beautifulsoup4
$ pip install regex
$ pip install selenium
```
### Richmenu (Make the Linebot have rich menus(圖文選單))
* This can be done at project's folder or out of project's folder, it doesn't matter. 
1. Create a file named 'richmenu.py', enter the following code in it and change some code by tips.
Run richmenu.py on terminal, then get the richmenu id.
```
# -*- coding: UTF-8 -*-
import requests
import json

headers = {"Authorization":"Bearer xxxxx","Content-Type":"application/json"}       # 移除xxxxx 打上你的 access token

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "選單",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 833, "height": 833},
          "action": {"type": "message", "text": "記支出"}
        },
        {
          "bounds": {"x": 833, "y": 0, "width": 833, "height": 833},
          "action": {"type": "message", "text": "圖表"}
        },
        {
          "bounds": {"x": 1666, "y": 0, "width": 833, "height": 833},
          "action": {"type": "message", "text": "比價"}
        },
        {
          "bounds": {"x": 0, "y": 843, "width": 833, "height": 833},
          "action": {"type": "message", "text": "記收入"}
        },
        {
          "bounds": {"x": 833, "y": 843, "width": 833, "height": 833},
          "action": {"type": "message", "text": "修改資料"}
        },
        {
          "bounds": {"x": 1666, "y": 843, "width": 833, "height": 833},
          "action": {"type": "message", "text": "查詢"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)                    #  得到選單 id

```
2. Create another file named rich2.py, enter the following code in it and change some code by tips.
* You will need to download 'richmenu.jpg' from https://playlab.computing.ncku.edu.tw:4001/group_2_final_project/linebot/blob/master/richmenu.jpg before running. 
* Picture(richmenu.jpg) need to be in the same folder with rich2.py.

Run rich2.py on terminal.
```
# -*- coding: UTF-8 -*-
from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('xxxxx')         # 移除xxxxx 改成自己的token

with open("richmenu.jpg", 'rb') as f:                              # 輸入圖片檔名
    line_bot_api.set_rich_menu_image("xxxxx", "image/jpeg", f)        # 移除xxxxx 輸入richmenu id

import requests
headers = {"Authorization":"Bearer xxxxx","Content-Type":"application/json"}         # 移除xxxxx 改成自己的token
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/xxxxx',
                       headers=headers)                                              # 移除xxxxx 輸入richmenu id

print(req.text)
```
3. Go to your Line bot APP to check if it has work.
<img src="https://i.imgur.com/fvAASDR.jpg" width="20%"/>


### Execute the Line Bot:
* There's a folder named moneyapp in invoicehero folder, and open views.py in moneyapp folder.
* In views.py, change line 76 to your own PATH. (just input the PATH where invoicehero at but exclude \invoicehero) 

   ![](https://i.imgur.com/6YFE8uy.jpg)
   <img src="https://i.imgur.com/wNrBbtg.jpg" width="80%"/>

* Go to finalproject folder in invoicehero folder and open setting.py, change line 24 and 25 to users' channel secret and channel access token.

![](https://i.imgur.com/PhfB0Ju.jpg)

* Go back to invoicehero folder and run `$ python manage.py runserver`.
* Wait until it shows the following message:

![](https://i.imgur.com/xWbwovH.jpg)
* Go back to Webhook URL, click the button "Verify", Line Bot will work if succeed.

![](https://i.imgur.com/7J7cVVJ.jpg)

## Getting Started with docker

### Docker container website
https://hub.docker.com/repository/docker/tim50687/final_project

### Dockerfile
https://hackmd.io/mRcfgf36So62x0v8V9UlRQ?view

### Prerequisite
* Install docker in your system
* Open terminal and run `$ docker pull tim50687/final_project`
* Create a linebot account 
1. Copy the **channel secret** and **channel access token** of your account's basic setting to a notebook. They will be used later.
2. Go to '回應設定' in your LINE Official Account Manager, close '自動回應訊息' and open 'Webhook'.

<img src="https://i.imgur.com/CdcdXuu.jpg" width="40%"/> <img src="https://i.imgur.com/Szh55m5.jpg" width="40%"/>

### Richmenu (Make the Linebot have rich menus(圖文選單))
* This can be done at project's folder or out of project's folder, it doesn't matter. 
1. Create a file named 'richmenu.py', enter the following code in it and change some code by tips.
Run richmenu.py on terminal, then get the richmenu id.
```
# -*- coding: UTF-8 -*-
import requests
import json

headers = {"Authorization":"Bearer xxxxx","Content-Type":"application/json"}       # 移除xxxxx 打上你的 access token

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "選單",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 833, "height": 833},
          "action": {"type": "message", "text": "記支出"}
        },
        {
          "bounds": {"x": 833, "y": 0, "width": 833, "height": 833},
          "action": {"type": "message", "text": "圖表"}
        },
        {
          "bounds": {"x": 1666, "y": 0, "width": 833, "height": 833},
          "action": {"type": "message", "text": "比價"}
        },
        {
          "bounds": {"x": 0, "y": 843, "width": 833, "height": 833},
          "action": {"type": "message", "text": "記收入"}
        },
        {
          "bounds": {"x": 833, "y": 843, "width": 833, "height": 833},
          "action": {"type": "message", "text": "修改資料"}
        },
        {
          "bounds": {"x": 1666, "y": 843, "width": 833, "height": 833},
          "action": {"type": "message", "text": "查詢"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)                    #  得到選單 id

```
2. Create another file named rich2.py, enter the following code in it and change some code by tips.
* You will need to download 'richmenu.jpg' from https://playlab.computing.ncku.edu.tw:4001/group_2_final_project/linebot/blob/master/richmenu.jpg before running. 
* Picture(richmenu.jpg) need to be in the same folder with rich2.py.

Run rich2.py on terminal.
```
# -*- coding: UTF-8 -*-
from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('xxxxx')         # 移除xxxxx 改成自己的 access token

with open("richmenu.jpg", 'rb') as f:                              # 輸入圖片檔名
    line_bot_api.set_rich_menu_image("xxxxx", "image/jpeg", f)        # 移除xxxxx 輸入richmenu id

import requests
headers = {"Authorization":"Bearer xxxxx","Content-Type":"application/json"}         # 移除xxxxx 改成自己的 access token
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/xxxxx',
                       headers=headers)                                               # 移除xxxxx 輸入richmenu id

print(req.text)
```
3. Go to your Line bot APP to check if it has work.
<img src="https://i.imgur.com/fvAASDR.jpg" width="20%"/>

### Execute the Line Bot:
1. Open terminal and run `$ docker run -it tim50687/final_project`.
2. Open **second** terminal, run `$ docker ps` and copy the **CONTAINER ID** of tim50687/final_project.
   Then, run `$ docker exec -it xxxxx /bin/bash` on your second terminal. Change xxxxx to your **CONTAINER ID**.
3. Sign up for [ngrok](https://ngrok.com/) and download file which is coressponding to your computer's version. 
4. Enter `$ ngrok authtoken <your authtoken>` and `$ ngrok http 8000` on **second** terminal.
![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_e4f71cf1b9cde8300de6b8db6919663d.png)
5. Copy the link generate by ngrok to Webhook URL in Line Messaging API and add `/callback`.
6. Open Use webhook
![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_d266b21c2251bbcaf372b6c18742e492.png)

* Revise the code and Execute Linebot APP
1. Go back to terminal which you've run `$ docker run -it tim50687/final_project`.

2. Find changetoken.sh in /root. And change **abc** with your **channel access token** and **channel secret**.
* Before changing, if your **channel access token** and **channel secret** have **/**, you need to add a **\\** before every **/**. 
![](https://i.imgur.com/Gy8R4Od.jpg)
![](https://i.imgur.com/cWb9ShR.jpg)

3. Run `$ ./changetoken.sh` under the path:/root.

4. Go in to **invoicehero** folder. Then, run `$ python3.9 manage.py runserver`.

5. Wait until it shows the following message:

![](https://i.imgur.com/xWbwovH.jpg)

6. Go back to Webhook URL, click the button "Verify", Line Bot will work if succeed.

![](https://i.imgur.com/7J7cVVJ.jpg)

## Check
Check whether the input data has been correctly upload or not.
* Expenses data: 
https://docs.google.com/spreadsheets/d/19OiyE1Pqp44BTDD9cXtpebntvuQHmPYRTLDy_OJCi2c/edit?usp=sharing

* Income data: 
https://docs.google.com/spreadsheets/d/1OGn7xzKwI8xySKstNWhpnqglK3AzooVPT11MCBAOGH4/edit?usp=sharing

* Budget data: 
https://docs.google.com/spreadsheets/d/14VUMIPWXfOynfr_Eixa8S2La7ksA-3i5zTWWTUd-8JA/edit?usp=sharing

* Picture of the chart function: 
https://drive.google.com/drive/folders/1C-84x5gomshiGb1wxDxemewMyLwwsU1m



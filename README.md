# Linebot-project

## Table of contents
* [About The Project](#about-the-project)
* [Technologies](#technologies)
* [Getting Started](#getting-started)
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
* Create a linebot account 
1. Copy the channel secret and channel access token of your account's basic setting to connect python script and Line Bot.
2. Open final project folder and open setting.py.
3. Change line 24 and 25 to users' channel secret and channel access token.

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
$ pip install oauth2client.service_account
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
$ pip install beautifulsoup4
$ pip install regex
$ pip install selenium
```
### Execute the Line Bot:
* Find views.py in moneyapp folder and open it.
* In views.py, change line 72 to your own PATH.

![](https://i.imgur.com/wMhuEYC.png) (just input the PATH exclude \invoicehero)
* Open terminal and enter `$ python manage.py runserver`.
* Go back to Webhook URL, click the button "Verify", Line Bot will work if succeed.

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


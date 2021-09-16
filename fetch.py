import pandas as pd
import requests
from bs4 import BeautifulSoup
#import telegram
#import Updater, MessageHandler, Filters, CallbackQueryHandler
from typing import Dict
import pandas as pd
import requests
import json 
import schedule
import datetime
from time import sleep



while True:
 # link = "https://chartink.com/screener/test-121377"
 link = "https://chartink.com/screener/"
 url = 'https://chartink.com/screener/process'

 payload = {
    # NOTE Intraday Mean Reversion - https://chartink.com/screener/intraday-mean-reversion-131
    'scan_clause': '( {33489} ( [0] 30 minute volume >= [0] 30 minute {custom_indicator_19473_start}"(  volume + 12 candles ago volume + 24 candles ago volume + 36 candles ago volume + 48 candles ago volume ) / 5"{custom_indicator_19473_end} * 2 and latest close > 70 and latest volume > 30000 and latest close <= 700 ) )'
    #'scan_clause': '( {33489} ( [0] 5 minute open / [0] 5 minute high <= 0.97 and [0] 5 minute close / [0] 5 minute high <= 0.97 ) )'
    #'scan_clause': '( {33489} ( [0] 15 minute low >= [-1] 30 minute low and [0] 15 minute high < [-1] 15 minute high and [-1] 15 minute high < [-2] 15 minute high and [-2] 15 minute high < [-3] 15 minute high and latest close > 90 and latest close < 900 ) )'     # NOTE Swapnaja screener - https://chartink.com/screener/swapnaja-sharma-swing-breakout
    # 'scan_clause': '( {cash} ( [0] 1 hour ema( [0] 1 hour close , 50 ) > [0] 1 hour ema( [0] 1 hour close , 200 ) and [0] 1 hour close > [0] 1 hour ema( [0] 1 hour close , 50 ) and [0] 1 hour rsi( 3 ) > 80 and [0] 1 hour macd line( 26,12,9 ) > [0] 1 hour macd signal( 26,12,9 ) and [0] 1 hour close > [-1] 1 hour high and [-1] 1 hour close > [-1] 1 hour open ) ) '
    #'scan_clause': '( {33489} ( latest close > 10 ) )'
    #'scan_clause': '( {33489} ( latest supertrend( 10,2 ) < latest close and 1 day ago  supertrend( 10,2 ) >= 1 day ago  close ) ) '
    # 'scan_clause': '( {33489} ( latest close > latest ema( close,07 ) and latest rsi( 6 ) > 75 and latest close > 120 and latest close < 9000 and latest volume > 100000 ) and latest close > latest vwap)'
    # 'scan_clause': '( {33489} ( ( {33489} ( [0] 15 minute ema( close,15 ) > [0] 15 minute ema( high,50 ) and [ -1 ] 15 minute ema( close,15 )<= [ -1 ] 15 minute ema( high,50 ) and [0] 15 minute close >= [0] 15 minute vwap and [0] 15 minute volume >= [0] 15 minute sma( volume,15 ) ) ) or( {33489} ( [0] 15 minute ema( close,15 ) < [0] 15 minute ema( low,50 ) and [ -1 ] 15 minute ema( close,15 )>= [ -1 ] 15 minute ema( low,50 ) and [0] 15 minute close <= [0] 15 minute vwap and [0] 15 minute volume >= [0] 15 minute ema( volume,15 ) ) ) or( {33489} ( [-1] 15 minute ema( close,15 ) > [-1] 15 minute ema( high,50 ) and [ -2 ] 15 minute ema( close,15 )<= [ -2 ] 15 minute ema( high,50 ) and [-1] 15 minute close >= [-1] 15 minute vwap and [-1] 15 minute volume >= [-1] 15 minute sma( volume,15 ) ) ) or( {33489} ( [-1] 15 minute ema( low,50 ) < [-1] 15 minute ema( close,15 ) and [ -2 ] 15 minute ema( low,50 )>= [ -2 ] 15 minute ema( close,15 ) and [-1] 15 minute close <= [-1] 15 minute vwap and [-1] 15 minute volume >= [-1] 15 minute ema( volume,15 ) ) ) ) )'
 }
 with requests.Session() as s:
    r = s.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.select_one("[name='csrf-token']")['content']
    s.headers['x-csrf-token'] = csrf
    r = s.post(url, data=payload)
    df = pd.DataFrame(columns=['sr', 'nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume'], index=None)
    print(df)
    
    # df = pd.DataFrame()
    for item in r.json()['data']:
        # print(item['name'],item['nsecode'],item['per_chg'],item['close'],item['volume'])
        # print(item)
        df = df.append(item, ignore_index=True)
    df.index = df['sr']
    df.drop('sr', axis=1, inplace=True)
    df.drop('name', axis=1, inplace=True)
    df.drop('bsecode', axis=1, inplace=True)
    #print(df)
    
    #table = df.to_markdown(index=False, tablefmt="grid")
    #table = df.to_markdown(tablefmt="grid") #index=False


    #df=df.Temp.astype(float)


    #print(table)

    TOKEN = "1732539858:AAEfJhYvXkycMd4Oc4-uDDiUFnxTuGZp3rY"
    URL =  "https://api.telegram.org/bot{}/".format(TOKEN)
    def get_url(url):
     response = requests.get(url)
     content = response.content.decode("utf8")
     return content


    def get_json_from_url(url):
     content = get_url(url)
     js = json.loads(content)
     return js


    def get_updates():
     url = URL + "getUpdates"
     js = get_json_from_url(url)
     return js


    def get_last_chat_id_and_text(updates):
     #num_updates = len(updates["result"])
     #last_update = num_updates - 1
     text = df#updates["result"][last_update]["message"]["text"]
     chat_id = -1001295106517#updates["result"][last_update]["message"]["chat"]["id"]
     return (text, chat_id)


    def send_message(text, chat_id):
     url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
     get_url(url)
    

    text, chat = get_last_chat_id_and_text(get_updates())
    send_message(text, chat)


    
    ### shedule automatic update
    sleep(900)   


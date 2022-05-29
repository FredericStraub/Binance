from binance.client import Client
from binance.enums import *
from telethon import TelegramClient
import math
import time
import re

with open("details.txt","r") as f:
    content = f.readlines()
content = [x.strip() for x in content]

api_key = content[1]
sec_key = content[2]

result = ""

api_id = 2871489
api_hash = '9a86212c74d8126191a7cdc20c86bec7'


client_tel = TelegramClient("APITELE",api_id,api_hash)
client_bin = Client(api_key,sec_key)    

l = []
prices = client_bin.get_all_tickers()
for i in prices:
        if str(i["symbol"])[-3:] == "BTC":
            l.append(i)
            l[-1]["symbol"] = l[-1]["symbol"][:(len(l[-1]["symbol"])-3)]

def translatestring(s,names):

    regex = re.compile('[^a-zA-Z]')
    string =regex.sub(' ', s)
    l = string.split()
    print(l)
    for i in l:
        if len(i) < 3:
            l.remove(i)
    
    for i in l:
        for j in names:
            if j.get("symbol") == i.upper():
                return i.upper()
    return ""

def get_wallet(client,Coin):
    info = client.get_account()
    for i in info.get("balances"):
        if i.get("asset") == Coin:
            myballance = float(i.get("free"))
            return myballance
def get_trade_price(client,Coin,l):
    
    for j in l:
        if j["symbol"] == Coin:
            price = j.get("price")

            return price
    return None
def get_trade_amount(client,Coin,l):
    info = client.get_account()
    myballance = get_wallet(client, "BTC")
    
    for j in l:
        if j["symbol"] == Coin:
            x = j["symbol"]+ "BTC"
            value = j.get("price")

    print(myballance,value)
    return math.floor((myballance/float(value))*0.3)

def autotrade(client,Coin,l):
    order = client.create_order(
        symbol = Coin+"BTC",
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=get_trade_amount(client,Coin,l)
    )
    print("gekauft")
    
    time.sleep(3.5)
    order = client.create_order(
                symbol = Coin+"BTC",
                side= SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=math.floor(get_wallet(client,Coin))
            )

    
def big_pump_letters(text):
    output = ""
    if "$" in text:
        x = text.partition("$")
        for i in x[2]:
            if i == " ":
                break
            else:
                output += i
    return output.upper()

# def bet_pumps_letters(text):
#     s = ""
#     print(text)
#     for i in text:
#         if i == " ":
#             s += i
#         if ord(i)>64 and ord(i)<91:
#             s += i
#     print(s)
#     l = s.split()
#     print(l)
#     for i in l:
#         if len(i) < 3:
#             l.remove(i)
#     if len(l) == 0:
#         return ""
#     print(l)
#     return l[0]
    

async def main():

    global result
    
    me = await client_tel.get_me()
    big_pump = await client_tel.get_input_entity("https://t.me/bigpumpsignal")
    bet_pump = await client_tel.get_input_entity("https://t.me/joinchat/SLcXCMK2jlbNJgsN")
    messages= await client_tel.get_messages(bet_pump,1)
    for i in messages:
        text = i.text
    result = text
        
    
while True:
    with client_tel:
        client_tel.loop.run_until_complete(main())
        result = translatestring(result,prices)
        if result != "" and result != "BTC":
            print(result)
            autotrade(client_bin,result,l)
            break
        else:
            print("nope")
            
        

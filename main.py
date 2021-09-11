from datetime import date
from binance import Client
import json


# Grab API Data, Token pair to Trade, Amount to buy from local JSON
with open('config.json') as f:
    data = json.load(f)

apiKey = data['apiKey']
apiSecret = data['apiSecret']
####TestNet API Keys OVERRIDE###################################################
apiKey = 'FWSZColzUi6onFbxDkm4XWNmVcG46vhh7h1QcL7Zz26pWyjHDaK7rx2CQByM6y5X'   #
apiSecret = 'Mw9Bp2hDTWkqMfa3cNrArDRMB0bmbPYG43IOSwEjjm0w8JXRv8MteOzUHADo7FLS'#
###############################################################################
symbol = data['tokenSymbol']
buyAmount = data['buyAmount']
sellAmount = data['sellAmount']

# Connect to API using config.json
# Remove testnet=True to interact with mainnet
# Remove tld='us' if using binance.com rather than binance.us
client = Client(apiKey, apiSecret, tld='us', testnet=True)


def moon_phase(month, day, year):
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    description = ["new moon",
                   "waxing crescent ",
                   "1/4 moon",
                   "waxing gibbous ",
                   "full moon",
                   "waning gibbous (",
                   "3/4 moon",
                   "waning crescent "]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if day == 31:
        day = 1
    days_into_phase = ((ages[(year + 1) % 19] +
                        ((day + offsets[month - 1]) % 30) +
                        (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16 / 59.0)
    # print(index)  # test
    if index > 7:
        index = 7
    status = description[index]

    # light should be 100% 15 days into phase
    light = int(2 * days_into_phase * 100 / 29)
    if light > 100:
        light = abs(light - 200);
    date = "%d %s %d" % (day, months[month - 1], year)

    return status, light  # date, status, light


# Get today's date,
today = str(date.today().strftime('%m,%d,%Y'))
# Split date into three variables
month, day, year = tuple(map(int, today.split(',')))
# Get today's moon phase + light value
todays_moon, light = (moon_phase(month, day, year))
print(f'Today\'s current moon phase is:', todays_moon, 'with a total light value of:', light)

def moon_check(todays_moon, light):
    # Returns True if moon is in final 3 days of waxing gibbous indicating a buy
    if "waxing gibbous" in todays_moon and light >= 90:
        return True
    # Returns False if moon is in final 3 days of waning crescent indicating a sell
    elif "waning crescent" in todays_moon and light <= 19:
        sell_flag = True
        return False
    # Return None if neither is satisfied, indicating no action is to be taken.
    else:
        return None


# If one of the above is true, buy/sell


def buy_order(token_pair, amount):
    client.order_market_sell(symbol=token_pair, quantity=amount)


def sell_order(token_pair, amount):
    client.order_market_buy(symbol=token_pair, quantity=amount)


flag = moon_check(todays_moon, light)

if flag:
    buy_order(symbol, buyAmount)
    print(f'Bought', {buyAmount}, 'of',{symbol})
elif flag is False:
    sell_order(symbol, sellAmount)
    print(f'Sold', {sellAmount}, 'of', {symbol})
elif flag is None:
    print('Moonboys ain\'t ready for this jelly. Here\'s today\'s portfolio:')
    print(client.get_account())
#
# buy_order(tokenPair, buyAmount)
# sell_order(tokenPair, sellAmount)






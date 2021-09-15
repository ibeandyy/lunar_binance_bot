from datetime import date, datetime
from binance import Client
import time
import json
from LicenseManager import license_check


if __name__ == '__main__':

    license_key = input("Please enter license key:")
    while license_check(license_key):

        # Grab API Data, Token pair to Trade, Amount to buy from local JSON
        with open('config.json') as f:
            data = json.load(f)

        apiKey = data['apiKey']
        apiSecret = data['apiSecret']
        ####TestNet API Keys OVERRIDE###################################################
        #apiKey = 'FWSZColzUi6onFbxDkm4XWNmVcG46vhh7h1QcL7Zz26pWyjHDaK7rx2CQByM6y5X'   #
        #apiSecret = 'Mw9Bp2hDTWkqMfa3cNrArDRMB0bmbPYG43IOSwEjjm0w8JXRv8MteOzUHADo7FLS'#
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



        while True:
            # Get today's date,
            today = str(date.today().strftime('%m,%d,%Y'))
            # Split date into three variables
            month, day, year = tuple(map(int, today.split(',')))
            # Get today's moon phase + light value
            todays_moon, light = (moon_phase(month, day, year))
            flag = moon_check(todays_moon, light)
            print(f'Today\'s current moon phase is:', todays_moon, 'with a total light value of:', light)

            # Check if today's moon is new or full, None values indicate today's date shouldn't be traded.
            if flag is None:
                print('No transactions required, sleeping. Today\'s account information:')
                try:
                    print(client.get_account())
                except:
                    print("Error retrieving account information, retrying")
                    time.sleep(60)
                    continue
                # Sleep for an hour and check again.
                time.sleep(600)
                continue
            # If today's date is 3 days prior to the full moon, iterate over token pairs and buy amounts, buy each
            # pair and wait three seconds in-between to avoid API lockout, sleep 24H after performing all buys from list
            elif flag:
                for ticker, buy in zip(symbol, buyAmount):
                    try:
                        buy_order(ticker, buy)
                    except:
                        print("Something went wrong, retrying")
                        continue
                    print(f'Bought', {buy}, 'of', {ticker})
                    if ticker == data['tokenSymbol'][-1]:
                        time.sleep(86401)
                        break
                    else:
                        time.sleep(3)
                        print("Something went wrong")
            # If today's date is 3 days prior to the new moon, iterate over token pairs and buy amounts, sell each
            # pair and wait three seconds in-between to avoid API lockout, sleep 24H after performing all buys from list.
            elif flag is False:
                for ticker, sell in zip(symbol, sellAmount):
                    try:
                        sell_order(ticker, sell)
                    except:
                        print("Something went wrong, retrying")
                        continue
                    if ticker == data['tokenSymbol'][-1]:
                        time.sleep(86401)
                        break
                    else:
                        time.sleep(3)
                    print(f'Sold', {sell}, 'of', {ticker})
















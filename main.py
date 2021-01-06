import os
import json
import requests


class TradingView:
    scan_url = "https://scanner.tradingview.com/"
    indicators = ["RSI|interval", "RSI[1]|interval", "Mom|interval", "Mom[1]|interval", "MACD.macd|interval", "MACD.signal|interval",
                  "close|interval", "EMA5|interval", "SMA5|interval", "EMA10|interval", "SMA10|interval", "EMA20|interval", "SMA20|interval",
                  "EMA30|interval", "SMA30|interval", "EMA50|interval", "SMA50|interval", "EMA100|interval", "SMA100|interval", "EMA200|interval",
                  "SMA200|interval", "VWMA|interval", "Rec.HullMA9|interval", "HullMA9|interval", "Pivot.M.Classic.S3|interval",
                  "Pivot.M.Classic.S2|interval", "Pivot.M.Classic.S1|interval", "Pivot.M.Classic.Middle|interval", "Pivot.M.Classic.R1|interval",
                  "Pivot.M.Classic.R2|interval", "Pivot.M.Classic.R3|interval"]

    def data(symbol, interval):
        """Format TradingView's Scanner Post Data

        Args:
            symbol (string): EXCHANGE:SYMBOL (ex: NASDAQ:AAPL or BINANCE:BTCUSDT)
            interval (string): Time Interval (ex: 1m, 5m, 15m, 1h, 4h, 1d, 1W, 1M)

        Returns:
            string: JSON object as a string.
        """
        if interval == "1m":
            # 1 Minute
            data_interval = "|1"
        elif interval == "5m":
            # 5 Minutes
            data_interval = "|5"
        elif interval == "15m":
            # 15 Minutes
            data_interval = "|15"
        elif interval == "1h":
            # 1 Hour
            data_interval = "|60"
        elif interval == "4h":
            # 4 Hour
            data_interval = "|240"
        elif interval == "1W":
            # 1 Week
            data_interval = "|1W"
        elif interval == "1M":
            # 1 Month
            data_interval = "|1M"
        else:
            # Default, 1 Day
            data_interval = ""

        indicators_copy = TradingView.indicators.copy()
        for x in range(len(indicators_copy)):
            indicators_copy[x] = indicators_copy[x].replace("|interval", data_interval)
        data_json = {"symbols": {"query": {"types": []}}, "columns": indicators_copy}
        #
        # "tickers": [symbol.upper()],
        print(data_json)
        return data_json


def get_analysis(exchange, screener, symbol, interval):
    exch_smbl = exchange.upper() + ":" + symbol.upper()
    data = TradingView.data(exch_smbl, interval)
    scan_url = TradingView.scan_url + screener.lower() + "/scan"
    response = requests.post(scan_url, json=data)
    result = json.loads(response.text)["data"]
    return result


current_indicators = get_analysis('NSE', 'INDIA', 'RELIANCE', '1W')

# Rename the previous file and create a new one
os.remove("Previous.json")
os.rename('Today.json', 'Previous.json')

with open('Today.json', 'w') as input:
    json.dump(current_indicators, input)
    input.close()

with open('Previous.json', 'r') as openfile:
    # Reading from json file
    previous_indicators = json.load(openfile)
    openfile.close()


# Function for performing the actual strategy analysis
def smaFiftyEmaHundred(today_indicators, last_indicators):
    potential_buy = []
    potential_sell = []
    young_stocks = []
    buy_stocks = []
    sell_stocks = []
    for current_stock in today_indicators:
        if current_stock['d'][16] != None and current_stock['d'][17] is not None and current_stock['d'][16] >= current_stock['d'][17]:
            potential_buy.append(current_stock['s'])
        elif current_stock['d'][16] == None:
            young_stocks.append(current_stock['s'])
        elif current_stock['d'][16] is not None and current_stock['d'][17] is not None and current_stock['d'][16] <= current_stock['d'][17]:
            x = '{},{},{}'.format(current_stock['s'], current_stock['d'][16], current_stock['d'][17])
            potential_sell.append(x)
    for stocks_buy in potential_buy:
        for shares in last_indicators:
            if stocks_buy == shares['s'] and shares['d'][16] <= shares['d'][17]:
                buy_stocks.append(stocks_buy)
    for stocks_sell in potential_sell:
        for shares in last_indicators:
            if stocks_sell == shares['s'] and shares['d'][16] >= shares['d'][17]:
                sell_stocks.append(stocks_sell)
    print('Buy Stocks\n\n', buy_stocks)
    print('Sell Stocks\n\n', sell_stocks)


smaFiftyEmaHundred(current_indicators, previous_indicators)

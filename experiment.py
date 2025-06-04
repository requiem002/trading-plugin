import yfinance as yf
import csv




stock=yf.Ticker("ULVR.L")
print(stock.info["regularMarketPrice"])

from nicegui import ui

ui.label("ello World!")
ui.run()


# with open("piePortfolio.csv","r") as f:
#     reader = csv.reader(f)
#     next(reader)

    # for row in reader:

    #     ticker=row[0]
    #     stock=yf.Ticker(ticker)
        

    #     dividendHistory=stock.dividends

    #     dividendPerShare=dividendHistory[len(dividendHistory)-1]

    #     print(dividendPerShare)
        
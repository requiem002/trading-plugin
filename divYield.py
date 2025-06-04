import csv
import yfinance as yf

def get_DividendYield(price, dividend_PerShare):
    return (dividend_PerShare/price)*100

def main():
    pieValue = 0
    total_divYield = 0

    with open("piePortfolio.csv","r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            ticker = row[0]
            stock = yf.Ticker(ticker)
            # Dividend history
            dividend_history = stock.dividends
            if not dividend_history.empty:
                #The final item of the list is the latest dividend!
                dividend_PerShare = dividend_history[len(dividend_history)-1]
                # Quantity of each stock
                quantity = float(row[5])
                # Current price of each stock
                price = stock.info["regularMarketPrice"]
                divYield = get_DividendYield(price, dividend_PerShare)
                stockValue = float(row[3])
                pieValue += stockValue
                print(pieValue)
                weight = stockValue/pieValue
                weighted_divYield = divYield * weight
                total_divYield += weighted_divYield 
                
    
    
    print(f"Total dividend yield: {total_divYield:.4f}%")
    


main()


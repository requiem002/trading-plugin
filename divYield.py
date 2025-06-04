import csv
import yfinance as yf


YAHOO_TICKER_MAP = {
    "ULVR": "ULVR.L",    # Unilever PLC (London)
    # Add more here if you get more 404s for EU/UK stocks (e.g. "SIE": "SIE.DE")
}

def get_dividend_yield(price, annual_dividend):
    if price == 0 or annual_dividend is None:
        return 0
    return (annual_dividend / price) * 100

def main():
    filename = "piePortfolio.csv"
    portfolio = []
    total_portfolio_value = 0

    # Step 1: Read portfolio and sum values
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = row['Slice'].strip()
            try:
                value = float(row['Value'])
                quantity = float(row['Owned quantity'])
            except (ValueError, TypeError):
                continue  # Skip this row if numbers are invalid

            if ticker and value > 0 and quantity > 0:
                portfolio.append({
                    'ticker': ticker,
                    'value': value,
                    'quantity': quantity
                })
                total_portfolio_value += value

    # Step 2: Calculate weighted dividend yield
    total_weighted_yield = 0
    missing_tickers = []
    for stock in portfolio:
  
        ticker = stock['ticker']
        value = stock['value']
        try:
            ticker_yahoo = YAHOO_TICKER_MAP.get(ticker, ticker)
            yf_ticker = yf.Ticker(ticker_yahoo)
            info = yf_ticker.info

            # Try to get annual dividend; fallback to last cash dividend * freq
            annual_dividend = info.get("dividendRate", None)
            if annual_dividend is None or annual_dividend == 0:
                # Try to estimate from recent dividends (quarterly etc)
                dividends = yf_ticker.dividends
                if not dividends.empty:
                    last_dividend = dividends.iloc[-1]
                    # Estimate annual dividend
                    if len(dividends) >= 4:
                        annual_dividend = dividends[-4:].sum()
                    else:
                        annual_dividend = last_dividend * 4  # Estimate
                else:
                    annual_dividend = 0

            price = info.get("regularMarketPrice", 0)
            if price == 0:
                price = value / stock['quantity']

            stock_yield = get_dividend_yield(price, annual_dividend)
            weight = value / total_portfolio_value
            weighted_yield = stock_yield * weight
            total_weighted_yield += weighted_yield
            #print(f"Total Weighted Yield: {total_weighted_yield}")
            #time.sleep(1)

        except Exception as e:
            missing_tickers.append(ticker)
            print(f"error: {e}")
            continue

    print(f"\nWeighted average dividend yield of your portfolio: {total_weighted_yield:.2f}%")
    if missing_tickers:
        print("\nCouldn't fetch dividend data for the following tickers:")
        for ticker in missing_tickers:
            print("-", ticker)

if __name__ == "__main__":
    main()
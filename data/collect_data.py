import yfinance as yf
import os
import pandas as pd

# List of NASDAQ tickers
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "PEP", "COST"]

# Date range
start_date = "2015-01-01"
end_date = "2025-01-01"

# Output directory
output_dir = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(output_dir, exist_ok=True)

# Downloading and save each ticker's data
for ticker in tickers:
    print(f"⬇️ Downloading {ticker}...")
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            df.to_csv(os.path.join(output_dir, f"{ticker}.csv"))
            print(f"✅ {ticker} saved.")
        else:
            print(f"⚠️ No data for {ticker}")
    except Exception as e:
        print(f"❌ Failed to download {ticker}: {e}")

print("\n✅ Data download complete.")

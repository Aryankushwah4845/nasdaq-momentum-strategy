from utils.data_loader import load_clean_data

print("🔍 Loading cleaned data...")
data = load_clean_data()

print(f"\n📈 Loaded {len(data)} tickers:\n")
for ticker, df in data.items():
    print(f"📂 {ticker}: {df.shape[0]} rows, {df.columns.tolist()}")
    print(df.head(2), "\n")

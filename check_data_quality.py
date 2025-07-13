import os
import pandas as pd

data_dir = "B/data/raw"

print("🔍 Checking data quality...\n")
for file in os.listdir(data_dir):
    if file.endswith(".csv"):
        path = os.path.join(data_dir, file)
        df = pd.read_csv(path)

        print(f"📂 {file}")
        if 'Date' not in df.columns or 'Close' not in df.columns:
            print("❌ Missing 'Date' or 'Close' column.")
            continue

        if df['Date'].isnull().any() or df['Close'].isnull().any():
            print("⚠️ Contains missing values.")
        else:
            print("✅ Data looks good.\n")

import os
import pandas as pd

input_folder = "B/data/raw"
output_folder = "B/data/clean"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(filepath, skiprows=3, header=None)
            df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
            df = df.dropna(subset=['Date', 'Close']) 
            df.to_csv(os.path.join(output_folder, filename), index=False)
            print(f" Cleaned: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} — {e}")

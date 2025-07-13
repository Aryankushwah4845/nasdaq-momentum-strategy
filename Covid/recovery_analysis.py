
import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_recovery_days(df, covid_start='2020-02-19', covid_bottom='2020-03-23'):
    df = df.copy()
    df.index = pd.to_datetime(df.index)

    try:
        pre_covid_price = df.loc[covid_start, 'Close']
        bottom_price = df.loc[covid_bottom:, 'Close'].min()
        bottom_date = df.loc[covid_bottom:, 'Close'].idxmin()

        # Only search *after* the market bottom
        post_bottom = df.loc[bottom_date:]
        recovery_date = post_bottom[post_bottom['Close'] >= pre_covid_price].first_valid_index()

        if pd.notnull(recovery_date):
            recovery_days = (recovery_date - bottom_date).days
            return recovery_days, bottom_date.date(), recovery_date.date()
        else:
            return None, bottom_date.date(), None

    except KeyError:
        return None, None, None

def main():
    print(" Measuring COVID-19 recovery times...\n")

    data_dir = os.path.join('B', 'data', 'raw')
    tickers = []
    recovery_days = []
    annotations = []

    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            ticker = filename.replace('.csv', '')
            filepath = os.path.join(data_dir, filename)

            df = pd.read_csv(filepath, index_col=0, parse_dates=True)
            df = df[['Close']].dropna()

            days, bottom_date, recovery_date = calculate_recovery_days(df)
            tickers.append(ticker)

            if days is not None:
                recovery_days.append(days)
                annotations.append(f"{bottom_date} → {recovery_date} ({days}d)")
                print(f"✅ {ticker}: Recovered in {days} days (from {bottom_date} to {recovery_date})")
            else:
                recovery_days.append(float('nan'))
                annotations.append("No recovery")
                print(f"❌ {ticker}: Did not recover to pre-COVID level.")

    # Plot
    plt.figure(figsize=(10, 5))
    bars = plt.bar(tickers, recovery_days, color='mediumseagreen')
    plt.title("COVID-19 Recovery Time (Days to Return to Pre-COVID Price)")
    plt.ylabel("Days to Recover")
    plt.xticks(rotation=45)

    for bar, label in zip(bars, annotations):
        height = bar.get_height()
        if pd.notnull(height):
            plt.text(bar.get_x() + bar.get_width()/2, height + 5, f"{label}", ha='center', fontsize=8, rotation=90)

    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    main()

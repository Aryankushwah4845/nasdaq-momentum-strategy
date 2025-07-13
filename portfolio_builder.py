import os
import pandas as pd
import matplotlib.pyplot as plt

# Local imports
from utils.data_loader import load_cleaned_data
from strategy.momentum_strategy import apply_strategy_to_all

# Strategy parameters
LOOKBACK = 20
STOP_LOSS = 0.10
TAKE_PROFIT = 0.20
TRANSACTION_COST = 0.001
ALLOW_SHORT = False

print("📊 Building portfolio from individual strategies...")

# Load cleaned data
data_dir = os.path.join("B", "data", "raw")
data_dict = load_cleaned_data(data_dir)

# Apply strategy to all tickers
results = apply_strategy_to_all(
    data_dict,
    lookback=LOOKBACK,
    stop_loss=STOP_LOSS,
    take_profit=TAKE_PROFIT,
    transaction_cost=TRANSACTION_COST,
    allow_short=ALLOW_SHORT
)

# Combine strategy returns
returns_df = pd.DataFrame({
    ticker: df['strategy_returns_net'].values
    for ticker, df in results.items()
}, index=next(iter(results.values())).index)

returns_df = returns_df.fillna(0)
returns_df['Portfolio'] = returns_df.mean(axis=1)

# Compute cumulative return
cumulative = (1 + returns_df['Portfolio']).cumprod()

# Save as CSV
portfolio_df = pd.DataFrame({
    'Date': cumulative.index,
    'Cumulative_Return': cumulative.values
})
output_path = os.path.join("B", "data", "portfolio_strategy_returns.csv")
portfolio_df.to_csv(output_path, index=False)

print(f"\n✅ Saved portfolio strategy returns to: {output_path}")

# Plot the portfolio performance
plt.figure(figsize=(10, 5))
plt.plot(cumulative, label='Equal-Weighted Portfolio')
plt.title("Portfolio Cumulative Return")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Figure_portfolio.png")
plt.show()

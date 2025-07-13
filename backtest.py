import os
import sys
import matplotlib.pyplot as plt
from utils.data_loader import load_cleaned_data
from strategy.momentum_strategy import apply_strategy_to_all



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


#  Strategy parameters

LOOKBACK = 20
STOP_LOSS = 0.10
TAKE_PROFIT = 0.20
TRANSACTION_COST = 0.001
ALLOW_SHORT = False

print("🚀 Running Momentum Backtest...")

# Load Cleaned Price Data
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'B', 'data', 'raw'))
data_dict = load_cleaned_data(data_dir)

# Apply to All Assets

results = apply_strategy_to_all(
    data_dict,
    lookback=LOOKBACK,
    stop_loss=STOP_LOSS,
    take_profit=TAKE_PROFIT,
    transaction_cost=TRANSACTION_COST,
    allow_short=ALLOW_SHORT
)

# Evaluate and Plot

for ticker, df in results.items():
    print(f"\n📊 {ticker} Performance Summary:")
    cumulative = (1 + df['strategy_returns_net'].fillna(0)).cumprod()
    final_return = cumulative.iloc[-1]
    print(f"Final Net Return: {final_return:.2f}x")

    plt.figure(figsize=(10, 4))
    plt.plot(cumulative, label=f'{ticker} Strategy', linewidth=2)
    plt.title(f"{ticker} Momentum Strategy (Net of Costs)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

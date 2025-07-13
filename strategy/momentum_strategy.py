import pandas as pd
import numpy as np

def generate_momentum_signals(df, lookback=20, stop_loss=0.10, take_profit=0.20, transaction_cost=0.001, allow_short=False):
    df = df.copy()
    df = df.dropna(subset=['Close'])  # Ensure no missing Close prices

    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Drop rows again in case conversion introduced NaNs
    df = df.dropna(subset=['Close'])

    df = df.copy()
    df = df.dropna(subset=['Close'])

    # Momentum calculation
    df['momentum'] = df['Close'].pct_change(periods=lookback)

    # Signal: 1 (buy), -1 (short), 0 (out)
    df['signal'] = 0
    if allow_short:
        df.loc[df['momentum'] > 0, 'signal'] = 1
        df.loc[df['momentum'] < 0, 'signal'] = -1
    else:
        df.loc[df['momentum'] > 0, 'signal'] = 1

    position = 0
    entry_price = 0
    signals = []

    for i, row in df.iterrows():
        if position == 0:
            if row['signal'] == 1:
                position = 1
                entry_price = row['Close']
            elif row['signal'] == -1 and allow_short:
                position = -1
                entry_price = row['Close']
        elif position == 1:
            change = (row['Close'] - entry_price) / entry_price
            if change <= -stop_loss or change >= take_profit or row['signal'] != 1:
                position = 0
        elif position == -1:
            change = (entry_price - row['Close']) / entry_price
            if change <= -stop_loss or change >= take_profit or row['signal'] != -1:
                position = 0
        signals.append(position)

    df['position'] = signals
    df['returns'] = df['Close'].pct_change()
    df['strategy_returns'] = df['position'].shift(1) * df['returns']
    trades = df['position'].diff().abs().fillna(0)
    df['strategy_returns_net'] = df['strategy_returns'] - trades * transaction_cost

    return df


def apply_strategy_to_all(
    data_dict,
    lookback=20,
    stop_loss=0.10,
    take_profit=0.20,
    transaction_cost=0.001,
    allow_short=False
):
    results = {}
    for ticker, df in data_dict.items():
        result_df = generate_momentum_signals(
            df,
            lookback=lookback,
            stop_loss=stop_loss,
            take_profit=take_profit,
            transaction_cost=transaction_cost,
            allow_short=allow_short
        )
        results[ticker] = result_df
    return results

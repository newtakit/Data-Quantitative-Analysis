import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


login = ********
password = ********
server = *********


mt5.initialize(login=login, password=password, server=server)


symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_M15
start_date = datetime(2019, 1, 1)
end_date = datetime(2021, 1, 1)

rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
rates_frame = pd.DataFrame(rates)
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')


ema21 = rates_frame['close'].ewm(span=21, adjust=False).mean()
rates_frame['ema21'] = ema21


buy_signals = (rates_frame['close'] > rates_frame['ema21']) & (rates_frame['close'].shift(1) < rates_frame['ema21'])
sell_signals = (rates_frame['close'] < rates_frame['ema21']) & (rates_frame['close'].shift(1) > rates_frame['ema21'])


signals = pd.DataFrame(index=rates_frame.index)
signals['signal'] = 0
signals.loc[buy_signals, 'signal'] = 1
signals.loc[sell_signals, 'signal'] = -1
signals['positions'] = signals['signal']


trades = signals['positions'][signals['positions'] != 0]
entry_exit_pairs = trades.groupby(trades.ne(trades.shift()).cumsum())


initial_balance = 500
balance = initial_balance
profits = []
balance_history = [initial_balance]

win_trades = 0
loss_trades = 0

for name, group in entry_exit_pairs:
    if len(group) == 2:
        entry = group.index[0]
        exit = group.index[1]
        entry_price = rates_frame.loc[entry, 'close']
        exit_price = rates_frame.loc[exit, 'close']
        if group.iloc[0] == 1:
            profit = exit_price - entry_price
            if profit > 0:
                win_trades += 1
            else:
                loss_trades += 1
        else:
            profit = entry_price - exit_price
            if profit > 0:
                win_trades += 1
            else:
                loss_trades += 1
        balance += profit
        balance_history.append(balance)
        profits.append(profit)

total_profit = balance - initial_balance
profit_percentage = (total_profit / initial_balance) * 100

total_trades = win_trades + loss_trades
win_percentage = (win_trades / total_trades) * 100 if total_trades > 0 else 0
loss_percentage = (loss_trades / total_trades) * 100 if total_trades > 0 else 0

#  CSV
results = {
    'Win Percentage': [win_percentage],
    'Loss Percentage': [loss_percentage],
    'Total Trades': [total_trades],
    'Total Profit (USD)': [total_profit],
    'Profit Percentage': [profit_percentage]
}
results_df = pd.DataFrame(results)
results_df.to_csv('trading_results.csv', index=False)

print(f"Total Profit: {total_profit:.2f} USD")
print(f"Profit Percentage: {profit_percentage:.2f}%")
print("Results saved to trading_results.csv")

plt.figure(figsize=(12, 6))
plt.plot(rates_frame['time'], rates_frame['close'], label='Close Price')
plt.plot(rates_frame['time'], ema21, label='EMA21', linestyle='--')
plt.scatter(rates_frame['time'][buy_signals], rates_frame['close'][buy_signals], marker='^', color='g', label='Buy Signal', alpha=1)
plt.scatter(rates_frame['time'][sell_signals], rates_frame['close'][sell_signals], marker='v', color='r', label='Sell Signal', alpha=1)
plt.legend(loc='best')
plt.title('Trading Strategy Backtest')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid(True)
plt.show()
plt.figure(figsize=(12, 6))
plt.plot(range(len(balance_history)), balance_history, label='Account Balance')
plt.title('Account Balance Over Time')
plt.xlabel('Trade')
plt.ylabel('Balance (USD)')
plt.grid(True)
plt.show()

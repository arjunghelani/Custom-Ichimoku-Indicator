from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# h4 = pd.read_csv('hold_h4.csv')
# m5 = pd.read_csv('hold_m5.csv')



# h4.set_index(pd.DatetimeIndex(h4['Datetime']), inplace=True)
# m5.set_index(pd.DatetimeIndex(m5['Datetime']), inplace=True)

                
class FullIchimoku(Strategy):
    
    def init(self):
        pass
    
    def next(self):
        current_signal = self.data.position[-1]
        
        if current_signal == 1:

            if self.position.is_short:
                self.position.close()
                self.buy()
                
            if not self.position:
                self.buy()
                
                
        elif current_signal == -1:
            if self.position.is_long:
                self.position.close()
                self.sell()
                
            if not self.position:
                self.sell()
                
        elif current_signal == 0:
            if self.position:
                self.position.close()

def run_backtest(data, n):
    data.set_index(pd.DatetimeIndex(data['Datetime']), inplace=True)
    bt = Backtest(data, FullIchimoku, cash=n, commission = 0.002)
    stats = bt.run()    
    print(stats)
    bt.plot()
    
                
# # FullIchimoku, Ichimoku
# h4_full  = Backtest(h4, FullIchimoku, cash=n, commission = 0.002)

# m5_full = Backtest(m5, FullIchimoku, cash=n, commission = 0.002)



# h4_full_stats = h4_full.run()
# m5_full_stats = m5_full.run()

# h4_full.plot()
# m5_full.plot()


# print('\n')
# print('4 Hour Window')
# print('–––––––––––––––––––––––––––––––––')
# print('\n')
# print(h4_full_stats)
# print('\n')
# print('5 Minute Window')
# print('–––––––––––––––––––––––––––––––––')
# print('\n')
# print(m5_full_stats)
# print('\n')


# returns_4h = (float(h4_full_stats['Return [%]'])/100 + 1) * n 
# returns_5m = (float(m5_full_stats['Return [%]'])/100 + 1) * n
# holds_4h = (float(h4_full_stats['Buy & Hold Return [%]'])/100 + 1)  * n 
# holds_5m = (float(m5_full_stats['Buy & Hold Return [%]'])/100 + 1) * n

# h4_days = (pd.to_datetime(h4.Date.iloc[-1]) - pd.to_datetime(h4.Date.iloc[0])).days
# m5_days = (pd.to_datetime(m5.Date.iloc[-1]) - pd.to_datetime(m5.Date.iloc[0])).days

# h4_return_pct = ((returns_4h - 50_000) / 50_000) * 100
# m5_return_pct = ((returns_5m - 50_000) / 50_000) * 100

# annual = (h4_return_pct + m5_return_pct) / ((h4_days / 365) + (m5_days / 365))

# h4_positions = h4.position.value_counts(normalize=True)
# m5_positions = m5.position.value_counts(normalize=True)

# print('4 hour returns:', f'${np.round(returns_4h - n, 2)}')
# print('4 hour returns above hold:', f'${np.round(returns_4h - holds_4h, 2)}')
# print('\n')
# print('Time Spent in Each Position')
# print('–––––––––––––––––––––––––––')
# print('Hold:', f'{np.round(h4_positions.loc[0], 2) * 100}%')
# print('Buy:', f'{np.round(h4_positions.loc[1], 2) * 100}%')
# print('Sell:', f'{np.round(h4_positions.loc[-1], 2) * 100}%')
# print('\n')
# print('5 minute returns:', f'${np.round(returns_5m - n, 2)}')
# print('5 minute returns above hold:', f'${np.round(returns_5m - holds_5m, 2)}')
# print('\n')
# print('Time Spent in Each Position')
# print('–––––––––––––––––––––––––––')
# print('Hold:', f'{np.round(m5_positions.loc[0], 2) * 100}%')
# print('Buy:', f'{np.round(m5_positions.loc[1], 2) * 100}%')
# print('Sell:', f'{np.round(m5_positions.loc[-1], 2) * 100}%')
# print('\n')
# print('Total returns above hold:', f'${np.round(returns_4h + returns_5m - holds_4h - holds_5m, 2)}')
# print('Hold:', f'${np.round(holds_4h + holds_5m, 2)}')
# print('Total:', f'${np.round(returns_4h + returns_5m, 2)}')
# print('Estimated Annual Return:', f'{np.round(annual, 2)}%')
# print('\n')

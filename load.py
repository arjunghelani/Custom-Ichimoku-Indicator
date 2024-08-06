import pandas as pd
import numpy as np
import datetime
import calendar
from itertools import product


class FourHour:
    def __init__(self):
        
        self.data = pd.read_csv('/Users/arjun/Downloads/nzd_jpy/NZDJPY4h.csv',)
        self.data['Date'] = self.data['Date'].astype(str)
        self.data['Date'] = self.data['Date'].apply(lambda x:f'{x[:4]}-{x[4:6]}-{x[6:]}')
        self.data['Datetime'] = self.data['Date'] + ' ' + self.data['Timestamp']
        self.data['Date'] = pd.to_datetime(self.data['Date'], yearfirst=True)
        self.data['Date'] = self.data['Date'].apply(lambda x:x.date())
        self.data['Datetime'] = pd.to_datetime(self.data['Datetime'], yearfirst=True)

    def ichimoku(self):

        nph = self.data['High'].rolling(9).max()
        npl = self.data['Low'].rolling(9).min()
        tenkan_sen = (nph + npl) / 2

        p26h = self.data['High'].rolling(26).max()
        p26l = self.data['Low'].rolling(26).min() 
        kijun_sen = (p26h + p26l) / 2

        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

        p52h = self.data['High'].rolling(52).max()
        p52l = self.data['Low'].rolling(52).min()

        senkou_span_b = ((p52h + p52l) / 2).shift(26)

        chikou_span = self.data['Close'].shift(-26)

        self.data['senkou_span_a'] = senkou_span_a
        self.data['senkou_span_b'] = senkou_span_b
        self.data['chikou_span'] = chikou_span
        self.data['kijun_sen'] = kijun_sen
        self.data['tenkan_sen'] = tenkan_sen
        
    def signal(self):
        '''Long'''
        long1 = self.data['senkou_span_a'] > self.data['senkou_span_b']
        self.data['tenkan_kijun_cross'] = np.NaN
        long2 = self.data['tenkan_sen'] > self.data['kijun_sen']
        long3 = (self.data['Close'] > self.data['tenkan_sen']) & (self.data['Close'] > self.data['senkou_span_a']) & (self.data['Close'] > self.data['senkou_span_b'])
        long4 = self.data['High'] < self.data['chikou_span']
        self.data['buy'] = np.where(long1 & long2 & long3 & long4, 1, 0)

        self.data['long1'] = long1
        self.data['long2'] = long2
        self.data['long3'] = long3
        self.data['long4'] = long4

        '''Short'''
        short1 = self.data['senkou_span_a'] < self.data['senkou_span_b']
        short2 = self.data['tenkan_sen'] < self.data['kijun_sen']
        short3 = (self.data['Close'] < self.data['tenkan_sen']) & (self.data['Close'] < self.data['senkou_span_a']) & (self.data['Close'] < self.data['senkou_span_b'])
        short4 = self.data['Low'] > self.data['chikou_span']
        self.data['sell'] = np.where(short1 & short2 & short3 & short4, -1, 0)  

        self.data['short1'] = short1
        self.data['short2'] = short2
        self.data['short3'] = short3
        self.data['short4'] = short4



        self.data['position'] = self.data['buy'] + self.data['sell']
        
    
#     def apply_signal(self, time_period = '4h'):
        
#         idx = []

#         self.data['returns_r9'] = self.data.Close.pct_change(9)
#         self.data['returns_r26'] = self.data.Close.pct_change(26)
#         self.data['returns_r52'] = self.data.Close.pct_change(52)

#         self.data['Datetime'] = pd.to_datetime(self.data['Datetime'], yearfirst=True)

#         signal_full_time = 0
#         signal_75_time = 0
#         self.signals = pd.DataFrame()

#         ## Full signal

#         trends = self.data[abs(self.data['returns_r52']) >= 0.02]


#         dt = trends['Datetime']
#         hour4 = pd.Timedelta(time_period)
#         in_block = ((dt - dt.shift(-1)).abs() == hour4) | (dt.diff() == hour4)

#         filt = trends.loc[in_block]
#         breaks = filt['Datetime'].diff() != hour4
#         groups = breaks.cumsum()
#         trends['groups'] = groups
#         for i in range(max(groups)):
#             min_idx = trends[trends.groups == i+1].Datetime.iloc[0]
#             max_idx = trends[trends.groups == i+1].Datetime.iloc[-1]

#             span = (max_idx - min_idx).days*24 + (max_idx - min_idx).seconds/3600
#             signal_full_time += span

#             period = trends[trends.groups == i+1]
#             signals = self.signal(period)
#             # signals = signals[['Datetime', 'Open', 'position', 'returns_r9', 'returns_r26', 'returns_r52']]
#             signals['flag75'] = 0
#             # signals['position'] = 0
#             self.signals = pd.concat([self.signals, signals])


#         non_trends = self.data[abs(self.data['returns_r52']) < 0.02]
#         dt2 = non_trends['Datetime']
#         in_block2 = ((dt2 - dt2.shift(-1)).abs() == hour4) | (dt2.diff() == hour4)

#         filt2 = non_trends.loc[in_block2]
#         breaks2 = filt2['Datetime'].diff() != hour4
#         groups2 = breaks2.cumsum()
#         non_trends['groups'] = groups2

#         for i in range(max(groups2)):
#             min_idx = non_trends[non_trends.groups == i+1].Datetime.iloc[0]
#             max_idx = non_trends[non_trends.groups == i+1].Datetime.iloc[-1]

#             span2 = (max_idx - min_idx).days*24 + (max_idx - min_idx).seconds/3600 
#             signal_75_time += span2
#             period2 = non_trends[non_trends.groups == i+1]
#             signals75 = self.signal(period2)
#             self.signals = pd.concat([self.signals, signals75])

#         total_hours = (self.data.Datetime.iloc[-1] - self.data.Datetime.iloc[0]).days*24 + \
#         (self.data.Datetime.iloc[-1] - self.data.Datetime.iloc[0]).seconds/3600

#         self.signals = self.signals.sort_values('Datetime')
#         df_idx = list(self.signals.index)
#         data_idx = list(self.data.index)
#         idx_diff = set(data_idx) - set(df_idx)
#         for i in idx_diff:
#             self.signals.loc[i] = self.data.loc[i]
#             if abs(self.signals.loc[i, 'returns_r52']) < 0.02:
#                 self.signals.loc[i, 'flag75'] = 1
#             else:
#                 self.signals.loc[i, 'flag75'] = 0

#         self.signals.sort_index(inplace=True)


    

    def hold(self):

        self.data['buy_total'] = self.data[['long1', 'long2', 'long3', 'long4']].mean(axis=1)

        self.data['sell_total'] = self.data[['short1', 'short2', 'short3', 'short4']].mean(axis=1)

        self.data['buy_ema5'] = self.data['buy_total'].rolling(5).mean()
        self.data['sell_ema5'] = -1 * self.data['sell_total'].rolling(5).mean()

        for index, row in self.data.iterrows():
            if (int(index) > self.data.index[0]) and (int(index) < self.data.index[-1]):
                position = row['position']
                last_position = self.data.loc[int(index) - 1, 'position']
                buys = row['long1'] + row['long2'] + row['long3'] + row['long4']
                sells = row['short1'] + row['short2'] + row['short3'] + row['short4']
                if last_position == 1:
                    if buys < 2:
                        self.data.loc[index, 'position'] = 0
                    else:
                        self.data.loc[index, 'position'] = 1
                elif last_position == -1:
                    if sells < 2:
                        self.data.loc[index, 'position'] = 0
                    else:
                        self.data.loc[index, 'position'] = -1

                else:
                    self.data.loc[index, 'position'] = self.data.loc[index, 'position']

            
        
        
class FiveMin:
    def __init__(self):
        
        self.data = pd.read_csv('/Users/arjun/Downloads/nzd_jpy/NZDJPY_mt5_bars.csv', header=None)
        self.data = self.data.iloc[:, :6]
        self.data.columns = ['Date', 'Timestamp', 'Open' ,'High', 'Low', 'Close']
        self.data['Date'] = self.data['Date'].astype(str)
        self.data['Date'] = self.data['Date'].apply(lambda x:f'{x[:4]}-{x[4:6]}-{x[6:]}')
        self.data['Datetime'] = self.data['Date'] + ' ' + self.data['Timestamp']
        self.data['Date'] = pd.to_datetime(self.data['Date'], yearfirst=True)
        self.data['Date'] = self.data['Date'].apply(lambda x:x.date())
        self.data['Datetime'] = pd.to_datetime(self.data['Datetime'], yearfirst=True)
        
        
    def ichimoku(self):

        nph = self.data['High'].rolling(9).max()
        npl = self.data['Low'].rolling(9).min()
        tenkan_sen = (nph + npl) / 2

        p26h = self.data['High'].rolling(26).max()
        p26l = self.data['Low'].rolling(26).min() 
        kijun_sen = (p26h + p26l) / 2

        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

        p52h = self.data['High'].rolling(52).max()
        p52l = self.data['Low'].rolling(52).min()

        senkou_span_b = ((p52h + p52l) / 2).shift(26)

        chikou_span = self.data['Close'].shift(-26)

        self.data['senkou_span_a'] = senkou_span_a
        self.data['senkou_span_b'] = senkou_span_b
        self.data['chikou_span'] = chikou_span
        self.data['kijun_sen'] = kijun_sen
        self.data['tenkan_sen'] = tenkan_sen
        
    def signal(self):
        
        '''Long'''
        long1 = self.data['senkou_span_a'] > self.data['senkou_span_b']
        self.data['tenkan_kijun_cross'] = np.NaN
        long2 = self.data['tenkan_sen'] > self.data['kijun_sen']
        long3 = (self.data['Close'] > self.data['tenkan_sen']) & (self.data['Close'] > self.data['senkou_span_a']) & (self.data['Close'] > self.data['senkou_span_b'])
        long4 = self.data['High'] < self.data['chikou_span']
        self.data['buy'] = np.where(long1 & long2 & long3 & long4, 1, 0)

        self.data['long1'] = long1
        self.data['long2'] = long2
        self.data['long3'] = long3
        self.data['long4'] = long4

        '''Short'''
        short1 = self.data['senkou_span_a'] < self.data['senkou_span_b']
        short2 = self.data['tenkan_sen'] < self.data['kijun_sen']
        short3 = (self.data['Close'] < self.data['tenkan_sen']) & (self.data['Close'] < self.data['senkou_span_a']) & (self.data['Close'] < self.data['senkou_span_b'])
        short4 = self.data['Low'] > self.data['chikou_span']
        self.data['sell'] = np.where(short1 & short2 & short3 & short4, -1, 0)  

        self.data['short1'] = short1
        self.data['short2'] = short2
        self.data['short3'] = short3
        self.data['short4'] = short4

        self.data['position'] = self.data['buy'] + self.data['sell']



    def hold(self):

        self.data['buy_total'] = self.data[['long1', 'long2', 'long3', 'long4']].sum(axis=1)

        self.data['sell_total'] = self.data[['short1', 'short2', 'short3', 'short4']].sum(axis=1)

    #     print(self.data[['buy_total', 'sell_total']])

    #     print(self.data[['buy_total', 'sell_total']].isna().sum())

        self.data['buy_ema'] = self.data['buy_total'].ewm(12, adjust=False).mean()
        self.data['sell_ema'] = -1 * self.data['sell_total'].ewm(12, adjust=False).mean()

        self.data['long_pct_change'] = self.data['Close'].pct_change(900)
        self.data['short_pct_change'] = self.data['Close'].pct_change(75)


        for index, row in self.data.iterrows():
            if (int(index) > self.data.index[0]) and (int(index) < self.data.index[-1]):
                position = row['position']
                last_position = self.data.loc[int(index) - 1, 'position']
                buys = row['long1'] + row['long2'] + row['long3'] + row['long4']
                sells = row['short1'] + row['short2'] + row['short3'] + row['short4']



                if (abs(self.data.loc[index, 'long_pct_change']) < 0.01) or (abs(self.data.loc[index, 'short_pct_change'] < 0.01)) and not ((self.data.loc[index, 'buy'] == 1) or (self.data.loc[index, 'sell'] == -1)):
                    self.data.loc[index, 'position'] = 0


                if last_position == 1:
                    if buys < 2:
                        self.data.loc[index, 'position'] = 0
                    else:
                        self.data.loc[index, 'position'] = 1


                    if self.data.loc[index-1, 'buy_ema'] < 0.5:
                        self.data.loc[index, 'position'] = 0
                    else:
                        self.data.loc[index, 'position'] = last_position





                elif last_position == -1:
                    if sells < 2:
                        self.data.loc[index, 'position'] = 0
                    else:
                        self.data.loc[index, 'position'] = -1

                    if self.data.loc[index-1, 'sell_ema'] > -0.5:
                        self.data.loc[index, 'position'] = 0
                    else:
                        self.data.loc[index, 'position'] = last_position


    
        

        
        
        
    
        
        
        
        
    






        
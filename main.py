import load
import backtest

if __name__ == '__main__':
    h4 = load.FourHour()
    h4.ichimoku()
    h4.signal()
    h4.hold()
    
    m5 = load.FiveMin()
    m5.ichimoku()
    m5.signal()
    m5.hold()
    
    backtest.run_backtest(h4.data, n = 50000)
    backtest.run_backtest(m5.data, n= 50_000)
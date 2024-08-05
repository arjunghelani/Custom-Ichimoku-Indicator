# Custom Indicator in FOREX Market

This project leverages the Ichimoku Cloud to identify and understand trends in the foreign exchange market. Fundamentals of the cloud are used and built upon to create a custom indicator responsible for implementing trading strategies across various time intervals.

## Introduction

There are five metrics calculated in the Ichimoku:
- Conversion Line (Tenkan Sen) –– 9-period midpoint
- Base Line (Kijun Sen) –– 26-period midpoint
- Leading Span A (Senkou Span A) –– Average of Tenkan Sen & Kijun Sen, plotted 26 periods ahead
- Leading Span B (Senkou Span B) –– 52-period midpoint plotted 26 periods ahead
- Lagging Span (Chikou Span) –– Close price plotted 26 periods back

The <i> Cloud </i> represents the area between Senkou Span A and Senkou Span B.


<img width="980" alt="Screen Shot 2024-08-05 at 12 23 33 PM" src="https://github.com/user-attachments/assets/be35b885-f35c-4867-90be-0534ec7dc16b">

## Enter Strategy


A buy signal is orchestrated when the four following conditions are met:
- Senkou Span A > Senkou Span B
- Tenkan Sen > Kijun Sen
- Close > Tenkan Sen & Close > Cloud
- Chikou Span > Low

Conversely, a sell signal is orchestrated when all four inequalities are true in the opposite direction.

## Exit Strategy

The indicator operates across two time intervals – 4 hours and 5 minutes. The 5-minute window is subject to more volatility, requiring the two intervals to operate with slightly different exit strategies.

For both intervals, a buy/sell signal is held if any two of the corresponding conditions are still true. If one or fewer conditions hold, the position is closed. An additional condition is applied to the 5-minute window:

- The total number of conditions met (in the corresponding buy/sell position) is represented by an integer (n)
- The weighted moving average of n is calculated across 12 periods (ema_n)
- If ema_n > 0.5, then the position is held

This additional condition allows the 5-minute strategy to mitigate potential dramatic losses by integrating the momentum of signal strength into decision-making.

## Backtesting

Backtesting is performed on the indicator for both 5-minute and 4-hour intervals across roughly a two-year span.

4-Hour Window

<img width="1427" alt="Screen Shot 2024-08-05 at 1 11 33 PM" src="https://github.com/user-attachments/assets/62c8a544-0a7b-4d03-9c79-83a641d81557">

5-Minute Window

<img width="1428" alt="Screen Shot 2024-08-05 at 1 11 56 PM" src="https://github.com/user-attachments/assets/f6d60790-9b6d-4301-968d-0049b348117c">














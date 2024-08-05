# Custom Indicator in FOREX Market

This project leverages the Ichimoku Cloud to identify and understand trends in the foreign exchange market. Fundamentals of the cloud are used and built upon to create a custom indicator responsible for implementing trading strategies across various time intervals.

## Introduction

There are five metrics calculated in the Ichimoku:
- Conversion Line (Tenkan Sen) –– 9-period midpoint
- Base Line (Kijun Sen) –– 26-period midpoint
- Leading Span A (Senkou Span A) –– Average of Tenkan Sen & Kijun Sen, plotted 26 periods ahead
- Leading Span B (Senkou Span B) –– 52-period midpoint plotted 26 periods ahead
- Lagging Span (Chikou Span) –– Close price plotted 26 periods back

The <i> cloud </i> represents the area between Senkou Span A and Senkou Span B.

<img width="980" alt="Screen Shot 2024-08-05 at 12 23 33 PM" src="https://github.com/user-attachments/assets/be35b885-f35c-4867-90be-0534ec7dc16b">

## Signal Strategy



A buy signal is orchestrated when the four following conditions are met:
- Senkou Span A > Senkou Span B
- 







# BenBot1 - Description

Uses KAMA (Kaufmann Adaptive Moving Average) to make buy / sell decisions.
KAMA is a volatility indicator and can be used to predict future price movement. It identifies existing trends, possible impending changes and market reversal points for market entry or exit.

This Bot works in 3 major steps:
1. Calculate Efficiency Ratio (=ER) and Smoothing Constant (=SC)
2. Calculate KAMA using previous KAMA, ER and SC
3. Based on Market-KAMA relation make buy / sell decision

Bot currently is set up for 3 KAMA lines. 1 for buy / sell and 2 more for market analysis.

erp, fema and sema params should be very close to 10, 2, 30 ratio

## Parameters
| Name         | Type         | Range         | Description  |
|--------------|--------------|---------------|--------------|
| erp  | int          | 10 - inf       | eff ratio in multiples of 10 periods |
| fema  | int          | 2 - inf       | number of fast exp. mov. avg.  periods|
| sema  | int          | 30 - inf       | number of slow exp. mov. avg. periods |
| fperc  | int          | 0 - 1       | failsafe perc. how far KAMA can deviate from current price |
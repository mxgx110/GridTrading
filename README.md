# GridTrading
Grid Trading Bot(GTB)

Grid trading is a trading bot that automates the buying and selling of futures contracts. It is designed to place orders in the market at preset intervals within a configured price range.
Grid trading is when orders are placed above and below a set price, creating a grid of orders at incrementally increasing and decreasing prices. In this way, it constructs a trading grid. For example, a trader could place buy-orders at every $1,000 below the market price of Bitcoin, while also placing sell-orders at every $1,000 above Bitcoin’s market price. This takes advantage of ranging conditions.
Grid trading performs the best in volatile and sideways markets when prices fluctuate in a given range. This technique attempts to make profits on small price changes. The more grids you include, the greater the frequency of trades will be. However, it comes with an expense as the profit you make from each order is lower.
Thus, it is a tradeoff between making small profits from many trades, versus a strategy with lower frequency but generates a bigger profit per order.
Binance Grid Trading is now live on USDⓈ-M Futures. Users can customize and set grid parameters, to determine the upper and lower limits of the grid and the number of grids. Once the grid is created, the system will automatically buy or sell orders at preset prices. \
\
The grid trading bot belongin to Binance is designed for real trading. This repository is the implementation of grid trading bot in Python from scratch. It first gives a config file and accordingly begins to run this strategy. Grid trading strategy has been designed for such a state in which the price fluctuates in a range, meaning that there is no sharp upward or downward trend.\
Further Reading: https://www.binance.com/en/support/faq/f4c453bab89648beb722aa26634120c3

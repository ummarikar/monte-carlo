import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

stock = input('Enter stock ticker: ')
NUM_SIMULATIONS = int(input('Enter number of simulations: '))

def monte_carlo(S0, mu, sigma, days=252):

    simulations = []
    for _ in range(NUM_SIMULATIONS):
        predictions = [S0]
        for _ in range(days):
            stock_price = predictions[-1] * np.exp((mu - 0.5 * sigma ** 2) + sigma * np.random.normal())
            predictions.append(stock_price)

        simulations.append(predictions)

    simulations_df = pd.DataFrame(simulations).T

    plt.plot(simulations_df)
    plt.title('Monte-Carlo Simulation of %s'%(stock))
    plt.xlabel('Days From Today')
    plt.ylabel('Price')
    plt.show()

    simulations_df['Mean'] = simulations_df.mean(axis=1)

    plt.plot(simulations_df['Mean'])
    plt.title('Average Monte-Carlo Simulation')
    plt.xlabel('Days From Today')
    plt.ylabel('Price')
    plt.show()

    print('Prediction for %s stock price a year from now: $%.2f' %(stock, simulations_df['Mean'].iloc[-1]))

today = datetime.today()
year_ago = today - relativedelta(years=1)

data = yf.download(stock, year_ago, today)['Adj Close']
data.plot()
plt.title('Historical Prices of %s'%(stock))
plt.ylabel('Price')
plt.show()

returns = data.pct_change()
mu = returns.mean()
sigma = returns.std()

monte_carlo(data[-1], mu, sigma)


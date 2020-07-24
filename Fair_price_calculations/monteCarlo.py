import datetime
from random import gauss
from math import exp,sqrt
import yfinance as yf
import pandas as pd


def monterCarloPriceGenerator(sP, vol, rfi, time_diff):
	price = sP*exp((rfi - 0.5*vol**2)*time_diff+ vol*sqrt(time_diff)*gauss(0,1.0))
	return price

def call_payoff(sT, k):
	return max(sT-k, 0)
#Stock
s = yf.Ticker('AAPL')
opt = s.option_chain('2020-08-21')
call= opt.calls 

def finalPrice(S,v,r,T,K):
	simulations = 900000
	payoffs = []
	discount_factor = exp(-r * T)

	for i in range(simulations):
	    S_T = monterCarloPriceGenerator(S,v,r,T)
	    payoffs.append(call_payoff(S_T, K))
	price = discount_factor * (sum(payoffs) / float(simulations))
	print ('Price: %.4f' % price)

#print(call.iloc[30]['impliedVolatility'])
#print(call.head(40))
S = s.history(period = "max")['Close'].iloc[-1]
r = 0.17900  # rate of 0.14%
T = (datetime.date(2020,8,21) - datetime.date(2020,7,24)).days / 365.0
for i in range(len(call)):
	v = call.iloc[i]['impliedVolatility']
	K = call.iloc[i]['strike']
	print(K)
	finalPrice(S,v,r,T,K)


import numpy as np
import datetime
import scipy.stats as si
import numpy as np
import scipy.stats as si
import yfinance as yf
    
def black_scholes_calc(S, K, T, r, sigma, option = 'call'): 
	#S: Current Stock Price
    #K: Strike price
    #T: Time to maturity in Years
    #r: Risk Free interest rate
    #sigma: Volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option == 'call':
        result = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    if option == 'put':
        result = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
        
    return result

'''
Sample Run
'''
s = yf.Ticker('AAPL')
opt = s.option_chain('2020-08-21')
call= opt.calls 
S = s.history(period = "max")['Close'].iloc[-1]
T = (datetime.date(2020,11,20) - datetime.date(2020,7,24)).days / 365.0
print(S, T)
for i in range(len(call)):
	v = call.iloc[i]['impliedVolatility']
	r = 0.17900 
	K = call.iloc[i]['strike']
	print(K)
	print ('Price: %.4f' % black_scholes_calc(S, K, T, 0.014, v))




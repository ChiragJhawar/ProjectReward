'''
Key Charecteristics:

1) A straddle is an options strategy involving the purchase of both a put and call option for the same expiration date and strike price on the same underlying.
2) The strategy is profitable only when the stock either rises or falls from the strike price by more than the total premium paid.
3) A straddle implies what the expected volatility and trading range of a security may be by the expiration date.
'''
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:.3f}'.format
import numpy as np
import yfinance as yf
import pytz
import datetime
from os import system, name

def setStock(st):
    # global variables
    global stock
    stock = st
def setDate(d):
    global date
    date = d

def getDatafirst():

    # assigning stock value and getting options data
    s = yf.Ticker(stock)
    opt = s.option_chain(date)
    call, put = opt.calls, opt.puts
    
    # Making our own Fair price column 'It is not exactly the market price, but very close.'
    call['Fair Price'] = [i if i >= 0.01 else 0.01 for i in (call['ask']+call['bid'])/2]
    put['Fair Price']  = [i if i >= 0.01 else 0.01 for i in (put['ask'] + put['bid'])/2]
    
    # Shortlisting data to a specific possible (rational) price range
    currentPrice = s.history(period = "max")['Close'].iloc[-1]
    oldPrice = s.history(period = "max")['Low'].iloc[-20]
    r = currentPrice - oldPrice
    priceRange = [int((currentPrice - r).round()), int((currentPrice + r).round())]
    
    # Assigning values to calls and puts
    calls = call[call['strike'] <= priceRange[1]]
    puts = put[put['strike'] >= priceRange[0]]
    return calls, puts

# getData(prediction: dataframe (can be calls or puts)) => n: dataframe
def getData(prediction):
    
    # Shortlisting even more accoriding to good volume.
    #c = prediction[prediction['volume']>=int(prediction['volume'].mean())]
    c = prediction
    if c['ask'].mean() != 0: # need to use time library later on
        l = c[['strike', 'Fair Price', 'impliedVolatility']]
        m = l.set_index('strike').to_dict()
        n = m['Fair Price'] 
        print("Using Current Market Price")
        
    else:
        j = c[['strike', 'lastPrice']]
        m = j.set_index('strike').to_dict()
        n = m['lastPrice']
        print("Using Last Price")
        
    return n


def put_payoff(sT, k ,p):
    return np.where(sT<k, k-sT , 0)-p

def call_payoff(sT, k,p):
    return np.where(sT>k, sT-k , 0)-p

setStock('UCO')
setDate('2020-08-21')
def plotStraddle(best_ratio):
    sT = np.arange(15,55,1)
    k = best_ratio['Strike Price']
    cp = best_ratio['Call Premium']
    pp = best_ratio['Put Premium']
    puts_payoff = put_payoff(sT, k,pp)
    calls_payoff =  call_payoff(sT, k, cp)
    final_payoff = calls_payoff+ puts_payoff
    #plotting details
    fig, ax = plt.subplots()
    ax.plot(sT,puts_payoff,'--', label = 'Put')
    plt.axhline(color='black')
    ax.plot(sT,calls_payoff, '--', label = 'Call')
    ax.plot(sT,final_payoff, label = 'Final Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    ax.set_title('Long Straddle')
    plt.legend()
    plt.show() 

def longStraddle():
    best_ratio = { 'Strike Price' : 0, 'Call Premium':0, 'Put Premium':0, 'maxRisk':0}
    calls = getDatafirst()[0]
    puts = getDatafirst()[1] 
    print(calls[['strike', 'impliedVolatility']])
    print(puts[['strike', 'impliedVolatility']]) 
    nPut = n = getData(calls)
    nCall = n = getData(puts)
    for call in nCall:
        for put in nPut:
            if call == put:
                maxRisk = nCall[call]+ nPut[put]
                best_ratio['Strike Price'] = call
                best_ratio['Call Premium'] = nCall[call] 
                best_ratio['Put Premium'] = nPut[put]
                best_ratio['maxRisk'] = maxRisk
                break

    #plotStraddle(best_ratio)

longStraddle()















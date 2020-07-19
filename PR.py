import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:.3f}'.format
import numpy as np
import yfinance as yf
import pytz
import datetime
from os import system, name

#global Variables

stock, date = '', ''

# getStock(st: String, d: String in date format) => calls: dataframe, puts: dataframe
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
    c = prediction[prediction['volume']>=int(prediction['volume'].mean())]
    
    if c['ask'].mean() != 0: # need to use time library later on
        l = c[['strike', 'Fair Price']]
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

def getBounds(sK, lK, t):
    higher,lower = 0,0
    if t=="putC" or t=='callD':
        if currentPrice < sK:
            lower = currentPrice-priceRange
        else:
            lower = sK-priceRange
        if currentPrice>lK:
            higher = currentPrice +priceRange
        else:
            higher = lK +priceRange
    return upper,lower
   
def plotGraph(best_ratio, tittle, t):
    #long
    strike_price_long =best_ratio['Long(Buy)']
    premium_long= best_ratio['Long Premium']
    #Short
    strike_price_short = best_ratio['Short(Sell)']
    premium_short= best_ratio['Short Premium']
    #upper,lower = getBounds(strike_price_short,strike_price_long, t)
    #print(int(upper),int(lower))
    sT = np.arange(15,45,1)
    if t=='putC' or t=='putD':
        long_payoff = put_payoff(sT, strike_price_long,premium_long)
        short_payoff = put_payoff(sT, strike_price_short,premium_short)*-1
    if t== 'callC' or t=='callD':
        long_payoff = call_payoff(sT, strike_price_long,premium_long)
        short_payoff = call_payoff(sT, strike_price_short,premium_short)*-1
    final_payoff = short_payoff+long_payoff
    #plotting details
    fig, ax = plt.subplots()
    ax.plot(sT,long_payoff,'--', label = 'Long')
    plt.axhline(color='black')
    ax.plot(sT,short_payoff, '--', label = 'Short')
    ax.plot(sT,final_payoff, label = 'Final Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    ax.set_title(tittle)
    plt.legend()
    plt.show() 

def appendBest(best_ratio, l, s, lp, sp, r, mrx, mrw):
    
    best_ratio['Long(Buy)'] = l
    best_ratio['Short(Sell)'] = s
    best_ratio['Risk/Reward Ratio'] = r
    best_ratio['Short Premium'] = sp
    best_ratio['Long Premium'] = lp
    best_ratio['maxRisk'] = mrx
    best_ratio['maxReward'] = mrw

    
def rnR(type, sL, sS, pL, pS):
    
    # credit spreads
    if type == 'callC' or type == 'putC':
        MaxReward = pS - pL
        MaxRisk = (sL - sS - MaxReward)
        
        if type == 'putC':
            MaxRisk *= -1
    
    # debit spreads
    elif type == 'callD' or type == 'putD':    
        MaxRisk = pL - pS
        MaxReward = (sL - sS) - MaxRisk
        
        if type == 'callD':
            MaxReward *= -1
            
    return MaxRisk, MaxReward

#Spread 1
#Spread 1
def basicSpreads(t):
    calls = getDatafirst()[0]
    puts = getDatafirst()[1]   

    if t == 'callD' or t == 'callC':
        n = getData(calls)
    elif t == 'putC' or t == 'putD':
        n = getData(puts)
    
#     We need to check the risk, reward, break even point
#     Then we need to check the ratio of the risk/reward
#     Then we need to store the 'Transaction' of the least ratio

    # best_ratio: Dictionary to maintain the best available trade at a given time
    best_ratio = {'Short(Sell)':0, 'Long(Buy)':0, 'Risk/Reward Ratio':((2**31)-1), 'Short Premium':0, 'Long Premium':0, 'maxRisk':0, 'maxReward':0}
   
    # First loop to check what to short (sell)   
    for short in n:
        
        # Second loop to check what we're buying (long)
        for long in n:
            
            # In a credit call spread the long Strike cannot be lower or equal to the short strike price
            if t == 'putD' or t == 'callC':
                if long > short:

                    # Declaring variables to work with
                    strikeShort = short
                    strikeLong = long

                    premiumShort = n[short]
                    premiumLong = n[long]
                    
                    z = rnR(t, strikeLong, strikeShort, premiumLong, premiumShort)
                
                    MaxRisk = z[0]
                    MaxReward = z[1]

                    if MaxReward > 0:
                        Ratio =  MaxRisk/MaxReward
                        if Ratio < best_ratio['Risk/Reward Ratio']:
                            appendBest(best_ratio, long, short, premiumLong, premiumShort, Ratio, MaxRisk, MaxReward)

               
            elif t == 'putC' or t == 'callD': 
                if long < short:

                    # Declaring variables to work with
                    strikeShort = short
                    strikeLong = long

                    premiumShort = n[short]
                    premiumLong = n[long]

                    # Figuring out the max risk vs reward in each spread to minimise the risk/reward ratio.
                    z = rnR(t, strikeLong, strikeShort, premiumLong, premiumShort)
                
                    MaxRisk = z[0]
                    MaxReward = z[1]

                    if MaxReward > 0:
                        Ratio =  MaxRisk/MaxReward
                        if Ratio < best_ratio['Risk/Reward Ratio']:
                            appendBest(best_ratio, long, short, premiumLong, premiumShort, Ratio, MaxRisk, MaxReward)

#     plotGraph(best_ratio, 'Call Credit Spread', 'callC')
    plotGraph (best_ratio, 'Spread', t)
    return ("Best", t, "Spread: ", best_ratio)

# setDate('2020-08-21')
# setStock("UCO")
# basicSpreads('callD')
# print("\n")
# basicSpreads('putC')
# print("\n")
# basicSpreads('callC')
# print("\n")
# basicSpreads('putD')
# #Final Testing call for all spreads
# def finalSpreads():
#     print("\t\t~~~~~~~~~~~~~~~~~~~~~~~ Bullish for Date",date , "~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
#     Call_Debit_Spread()
#     print("\n")
#     Put_Credit_Spread()
#     print("\n")
#     print("\t\t~~~~~~~~~~~~~~~~~~~~~~~ Bearish for Date",date ,"~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
#     Put_Debit_Spread()
#     print("\n")
#     Call_Credit_Spread()





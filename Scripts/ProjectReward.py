import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import pytz
import datetime
from os import system, name

pd.options.display.float_format = '{:.3f}'.format

class ProjectRewarder:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BASIC FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, ticker, date, flag, spread_type):
        self.ticker = ticker #NYSE ticker
        self.date = date #date "YYYY-MM-DD"
        self.flag = flag #type of spread, ["calls", "puts"]
        self.spread_type = spread_type #credit/debit ["credit", "debit"]
        self.best_ratio = None

    def __repr__(self):
        return "<ProjectRewarder ticker={} date={} flag={} spread_type={}>".format(self.ticker, self.date, self.flag, self.spread_type)

    def setTicker(self, newTicker):
        try:
            self.ticker = newTicker
            return {'status': 200}
        except:
            return {'status': 501}

    def setDate(self, setdate):
        try:
            self.date = setdate
            return {'status': 200}
        except:
            return {'status': 501}

    def setFlag(self, newFlag):
        try:
            self.flag = newFlag
            return {'status': 200}
        except:
            return {'status': 501}

    def setType(self, newSpread):
        try:
            self.spread_type = newSpread
            return {'status': 200}
        except:
            return {'status': 501}

    def getTicker(self):
        return self.ticker

    def getInitialStockData(self):
        s = yf.Ticker(self.ticker)
        opt = s.option_chain(self.date)

        call, put = opt.calls, opt.puts

        call['Fair Price'] = [i if i >= 0.01 else 0.01 for i in (call['ask']+call['bid'])/2]
        put['Fair Price']  = [i if i >= 0.01 else 0.01 for i in (put['ask'] + put['bid'])/2]

        currentPrice = s.history(period = "max")['Close'].iloc[-1]
        oldPrice = s.history(period = "max")['Low'].iloc[-10]
        r = currentPrice - oldPrice
        priceRange = [int((currentPrice - r).round()), int((currentPrice + r).round())]

        # Assigning values to calls and puts
        if self.spread_type == 'debit':
        	calls = call[call['strike'] <= priceRange[1]]
        	puts = put[put['strike'] >= priceRange[0]]

        elif self.spread_type  == 'credit':   
            calls = call[call['strike'] >= priceRange[1]]
            puts = put[put['strike'] <= priceRange[0]]

        return calls, puts

    def getData(self, prediction):

        # Shortlisting calls/puts even more accoriding to good volume.
        # prediction = calls if self.flag == 'calls' else puts
        print(int(prediction['volume'].mean()), '\n\n')
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

    def appendBest(self, l, s, lp, sp, r, mrx, mrw):
        self.best_ratio['Long(Buy)'] = l
        self.best_ratio['Short(Sell)'] = s
        self.best_ratio['Risk/Reward Ratio'] = r
        self.best_ratio['Short Premium'] = sp
        self.best_ratio['Long Premium'] = lp
        self.best_ratio['maxRisk'] = mrx
        self.best_ratio['maxReward'] = mrw

    def rnR(self, sL, sS, pL, pS):

        # credit spreads
        if self.spread_type == 'credit':
            MaxReward = pS - pL
            MaxRisk = (sL - sS - MaxReward)

            if self.flag == 'puts':
                MaxRisk *= -1

        # debit spreads
        elif self.spread_type == 'debit':
            MaxRisk = pL - pS
            MaxReward = (sL - sS) - MaxRisk

            if self.flag == 'calls':
                MaxReward *= -1

        return MaxRisk, MaxReward

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GRAPHING FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def put_payoff(self, sT, k ,p):
        return np.where(sT<k, k-sT , 0)-p

    def call_payoff(self, sT, k,p):
        return np.where(sT>k, sT-k , 0)-p


    def plotGraphBasic(self):
    #toBuy
        strike_price_toBuy =self.best_ratio['Long(Buy)']
        premium_toBuy= self.best_ratio['Long Premium']
        #Short
        strike_price_toSell = self.best_ratio['Short(Sell)']
        premium_toSell= self.best_ratio['Short Premium']

        sT = np.arange(15,45,1)
        if (self.flag, self.spread_type) == ('puts', 'debit') or (self.flag, self.spread_type) == ('calls', 'credit'):
            toBuy_payoff = self.put_payoff(sT, strike_price_toBuy,premium_toBuy)
            toSell_payoff = self.put_payoff(sT, strike_price_toSell,premium_toSell)*-1
        if (self.flag, self.spread_type) == ('puts', 'credit') or (self.flag, self.spread_type) == ('calls', 'debit'):
            toBuy_payoff = self.call_payoff(sT, strike_price_toBuy,premium_toBuy)
            toSell_payoff = self.call_payoff(sT, strike_price_toSell,premium_toSell)*-1
        final_payoff = toSell_payoff+toBuy_payoff
        #plotting details
        fig, ax = plt.subplots()
        ax.plot(sT,toBuy_payoff,'--', label = 'Long')
        plt.axhline(color='black')
        ax.plot(sT,toSell_payoff, '--', label = 'Short')
        ax.plot(sT,final_payoff, label = 'Final Payoff')
        plt.xlabel('Stock Price (sT)')
        plt.ylabel('Profit & Loss')
        ax.set_title(tittle)
        plt.legend()
        plt.show() 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FINAL FUNCTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getBasicSpread(self):
        calls, puts = self.getInitialStockData()

        n = self.getData(calls if self.flag == "calls" else puts)

        self.best_ratio = {'Short(Sell)':0, 'Long(Buy)':0, 'Risk/Reward Ratio':((2**31)-1), 'Short Premium':0, 'Long Premium':0, 'maxRisk':0, 'maxReward':0}
        for toSell in n:
            for toBuy in n:

                if (self.flag, self.spread_type) == ('puts', 'debit') or (self.flag, self.spread_type) == ('calls', 'credit'):
                    if toBuy > toSell:
                        strikeShort = toSell
                        strikeLong = toBuy

                        premiumShort = round(n[toSell], 2)
                        premiumLong = round(n[toBuy], 2)

                        z = self.rnR(strikeLong, strikeShort, premiumLong, premiumShort)
                        MaxRisk = z[0]
                        MaxReward = z[1]

                        if MaxReward > 0:
                            Ratio =  round(MaxRisk/MaxReward,4)
                            if Ratio < self.best_ratio['Risk/Reward Ratio']:
                                self.appendBest(toBuy, toSell, premiumLong, premiumShort, Ratio, MaxRisk, MaxReward)

                elif (self.flag, self.spread_type) == ('puts', 'credit') or (self.flag, self.spread_type) == ('calls', 'debit'):

                    if toBuy < toSell:
                        strikeShort = toSell
                        strikeLong = toBuy

                        premiumShort = n[toSell]
                        premiumLong = n[toBuy]

                        z = self.rnR(strikeLong, strikeShort, premiumLong, premiumShort)
                        MaxRisk = z[0]
                        MaxReward = z[1]

                        if MaxReward > 0:
                            Ratio =  round(MaxRisk/MaxReward, 4)
                            if Ratio < self.best_ratio['Risk/Reward Ratio']:
                                self.appendBest(toBuy, toSell, premiumLong, premiumShort, Ratio, MaxRisk, MaxReward)
        return self.best_ratio

worker = ProjectRewarder("WKHS", "2020-07-23", "calls", "credit")

print(worker.getBasicSpread())
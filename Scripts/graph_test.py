import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm 
import time 
import math

def put_payoff(sT, k ,p):
	return np.where(sT<k, k-sT , 0)-p

def bear_put():
    
	#Random Stock Data
	currentPrice = 160
    
	 # Long Put
	strikeLongPut =165
	premiumLongPut = 9.7
    
	 # Short Put
	strikeShortPut = 155
	premiumShortPut = 5.4
    
	sT = np.arange(100,220,1)
    
	#Bearish Put Payoff matrix graph
	long_put_payoff = put_payoff(sT, strikeLongPut, premiumLongPut)
	fig, ax = plt.subplots()   
	ax.plot(sT,long_put_payoff,'--', label = 'Long Put')  
	plt.axhline(color='black')
    
	short_put_payoff = put_payoff(sT, strikeShortPut, premiumShortPut)*-1
	ax.plot(sT,short_put_payoff, '--', label = 'Short Put')
    
	final_payoff = short_put_payoff+long_put_payoff
	ax.plot(sT,final_payoff, label = 'Final Payoff')
    
	plt.xlabel('Stock Price (sT)')
	plt.ylabel('Profit & Loss')
	ax.set_title('Bear Put Payoff')
    
	plt.legend()
	plt.show()

def call_payoff(sT, k,p):
	return np.where(sT>k, sT-k , 0)-p

def bear_call():
	#Random Stock Data
	s0 = 94.6
	sT = np.arange(20,160,1)
	#Long Call
	k_long_call = 100
	p_long_call = 2.7
	#Short Call
	k_short_call = 70
	p_short_call = 28
	l_call_payoff = call_payoff(sT, k_long_call, p_long_call)
	s_call_payoff = call_payoff(sT, k_short_call, p_short_call)*-1
	fig, ax = plt.subplots()
	plt.axhline( '0', color='black')
	ax.plot(sT, s_call_payoff, '--',label = 'Short Call')
	ax.plot(sT, l_call_payoff,'--', label = 'Long Call')
	ax.plot(sT,s_call_payoff+l_call_payoff , label="Bear Payoff")
	plt.xlabel('Stock Price (sT)')
	plt.ylabel('Profit & Loss')
	ax.set_title('Bear Call Payoff')
	plt.legend()
	plt.show()

bear_call()


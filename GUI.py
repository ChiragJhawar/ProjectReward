import PR
from tkinter import*
import tkinter as tk

top = tk.Tk()
Label(top, text = "Welcome to Project Reward: \n Enter the stock of your choice and chose the spread type").pack()
canvas1 = tk.Canvas(top, width = 200, height = 120)
# greetings = Label(text = "Hello")
# greetings.pack()
canvas1.pack()
stock = tk.Entry(top)
canvas1.create_window(100,50,window=stock)

def getStock():
	st = stock.get()
	PR.setstock(st)

btn = Button(top, text = "Set stock", command = getStock)
canvas1.create_window(100,90,window=btn)
PR.setstock(stock.get())
def get_pds():
	win = tk.Toplevel(top)
	text = PR.Put_Debit_Spread()
	Label(win , text = text).pack()
	


btn1 = Button(top, text="Bearish Put Spread" , command = get_pds)
btn2 = Button(top, text="Bearish Call Spread", command = PR.Call_Credit_Spread)
btn3 = Button(top, text="Bullish Put Spread", command = PR.Put_Credit_Spread)
btn4 = Button(top, text="Bullish Call Spread", command = PR.Call_Debit_Spread)
btn1.pack()
btn2.pack()
btn3.pack()
btn4.pack()
top.mainloop()

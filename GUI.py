import PR
from tkinter import*
import tkinter as tk
from sys import platform as sys_pf


top = tk.Tk()
top.title("ProjectReward")
Label(top, text = "Welcome to Project Reward: \n Enter the stock of your choice and chose the spread type").pack()
canvas1 = tk.Canvas(top, width = 200, height = 160)
# greetings = Label(text = "Hello")
# greetings.pack()
canvas1.pack()
def setStock():
	st = stock.get()
	PR.setStock(st)

def setDate():
	d = date.get()
	PR.setDate(d)

stock = tk.Entry(top)
canvas1.create_window(100,50,window=stock)

btn = Button(top, text = "Set Stock", command = setStock)
canvas1.create_window(100,80,window=btn)

date = tk.Entry(top)
canvas1.create_window(100,110,window=date)

btnDate = Button(top, text = "Set Date", command = setDate)
canvas1.create_window(100,140,window=btnDate)

def get_pds():
	win = tk.Toplevel(top)
	text = PR.basicSpreads('putD')
	Label(win , text = text).pack()

def get_cds():

	win = tk.Toplevel(top)
	text = PR.basicSpreads('callD')
	Label(win , text = text).pack()

def get_pcs():
	win = tk.Toplevel(top)
	text = PR.basicSpreads('putC')
	Label(win , text = text).pack()

def get_ccs():
	win = tk.Toplevel(top)
	text = PR.basicSpreads('callC')
	Label(win , text = text).pack()

btn1 = Button(top, text="Bearish Put Spread" , command = get_pds)
btn2 = Button(top, text="Bearish Call Spread", command = get_ccs)
btn3 = Button(top, text="Bullish Put Spread", command = get_pcs)
btn4 = Button(top, text="Bullish Call Spread", command = get_cds)
btn1.pack()
btn2.pack()
btn3.pack()
btn4.pack()
top.mainloop()

'''
Created on Dec 15, 2017

@author: yingc
'''
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


dates = ['01/02/1991','01/03/1991','01/04/1991']
x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]

y = range(len(x)) # many thanks to Kyss Tao for setting me straight here
y= [1,3,2]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.plot(x,y)
plt.gcf().autofmt_xdate()
plt.show()
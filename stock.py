#Raj's stock analysis script
#import modules
import ystockquote
from numpy import *
import math
from pylab import *

#functions
def mavsmooth(r,n):
	window = ones(n)/float(n)
	return convolve(r.transpose()[0,0:len(r)-1],window)
		

def ksmooth(price,price_hat):
	p = 1
	for i in range(0,len(data)-2):
		price_hat[i+1],p = kfilt(price[i], price_hat[i],p)
	return price_hat

def kfilt(z,x,p):
	R = 60
	q = 0.1
	mu = math.log(1.05)/365 
	r = z-x
	k = float(p/(p+R))
	x = x+k*r
	p = (1-k)*p
	p = p+q
	x = x+mu*z
	return (x,p);
	
def arrange_data(price):
	for i in range(1,len(data)):
		price[len(price)-(i)] = float(data[i][4])
	return(price)


#main script
#start yyyymmdd
start = '20120101'
end = '20130220'
symbol = 'orcl'

#orient in chronological order
data = ystockquote.get_historical_prices(symbol, start, end)
price = zeros((len(data)-1,1))
price_hat = zeros((len(data)-1,1))
arrange_data(price)

#smooth the data and predict with a kalman filter
price_hat[0] = price[0]
price_hat = ksmooth(price,price_hat)

#residual analysis
r = price-price_hat
r_s = mavsmooth(r,50)

#plot data
subplot(211)
plot(price_hat,'r',price,'b')
grid(True)
title('Price of %s'%(symbol))
xlabel('Days')
ylabel('Price $')

subplot(212)
plot(r,'b',r_s,'r')
grid(True)
xlabel('Days')
ylabel('Residual')
show()



'''
Created on Jan 29, 2014

@author: Silver
'''

from scipy.stats import powerlaw
from numpy.random import normal
from numpy.random  import random
import matplotlib.pyplot as plt
from objects.Order import Order

lit_venues = ["Euronext", "ChiX", "BATS", "Turqoise"]
dark_venues = ["SigmaX", "UBS-MTF", "BLINK", "Xetra-Mid", "ChiX-DARK", "BATS-Dark"]

def generate_snapshot(lit_venue_count = 3, dark_venue_count = 3):
    orderbook = {}
    #lit venues first
    for lv in range(lit_venue_count):
        orderbook[lit_venues[lv]] = {}
        # buy first
        side = 1
        limit = 0
        price = 100
        while (limit < 5):         
            
            nb_orders = int(round(10*powerlaw.rvs(0.6)))
            
            if nb_orders > 0:
                orderbook[lit_venues[lv]][price] = []
                for i in range(nb_orders):
                    size = int(round(normal(100, 30))) # total qty
                    iceberg = powerlaw.rvs(0.8) # ratio of visible qty
                    decay = random()
                    
                    o = Order()
                    o.side = side
                    o.price = price
                    o.size = size
                    o.shown = int(iceberg * size)
                    o.decay = decay
                    o.id = "Order_%f_%d" %(price, i)
                    o.symbol = lit_venues[lv]
                    
                    orderbook[lit_venues[lv]][price].append(o)
                limit += 1                
            price -= 1
        
        side = -1
        limit = 0
        price = 101    
        while (limit < 5):         
            
            nb_orders = int(round(10*powerlaw.rvs(0.6)))
            
            if nb_orders > 0:
                orderbook[lit_venues[lv]][price] = []
                for i in range(nb_orders):
                    size = int(round(normal(100, 30))) # total qty
                    iceberg = powerlaw.rvs(0.8) # ratio of visible qty
                    decay = random()
                    
                    o = Order()
                    o.side = side
                    o.price = price
                    o.size = size
                    o.shown = int(iceberg * size)
                    o.decay = decay
                    o.id = "Order_%f_%d" %(price, i)
                    o.symbol = lit_venues[lv]
                    
                    orderbook[lit_venues[lv]][price].append(o)
                limit += 1                
            price += 1
            
    
    return orderbook

def plot_orderbook(orderbook):
    prices = orderbook.keys()
    prices_buy = []
    prices_sell = []
    sizes_buy = []
    sizes_sell = []
    for k in prices:
        if k <= 100:
            prices_buy.append(k)
            sizes_buy.append(sum([o.size for o in orderbook[k]]))
        else:
            prices_sell.append(k)
            sizes_sell.append(sum([o.size for o in orderbook[k]]))
    
    plt.bar(prices_buy, sizes_buy)
    plt.bar(prices_sell, sizes_sell, color = 'r')
    plt.show()
    

if __name__ == "__main__":
    ob = generate_snapshot(3, 3)
    plot_orderbook(ob["Euronext"])
    
    
    
            
                    
                    
                    
                    

                    
                    
                    
            
            
    
    
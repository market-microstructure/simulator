'''
Created on Sep 23, 2013

@author: Silver
'''

from tools.Order import *

class DummyAgent():
    def __init__(self, service_locator):
        self.services = service_locator
        self.x = 0
    
    def process(self, symbol):
        print "Received Market Data Event on symbol %s" % symbol
        data = self.services.bus.get_market_data()
        print data
        print "BID: %d, ASK: %d, PRICE: %d, SIZE: %d" % (data[symbol]["bid"], data[symbol]["ask"], data[symbol]["price"], data[symbol]["size"])
        
        if self.x == 0:
            o = Order()
            o.side = 1
            o.price = 16
            o.size = 50
            o.symbol = symbol
            o.id = "MyOrder"
            
            self.services.order_dispatcher.new_order(o)           
        
            self.x += 1
        
        
    def process_report(self, id):
        print "execution!!!!!!!!!!!!"
'''
Created on Sep 23, 2013

@author: Silver
'''

from objects.Order import *

class DummyAgent():
    def __init__(self, service_locator, params):
        self.services = service_locator
        self.parameters = params
    
    def process(self, symbol):        
        data = self.services.bus.get_market_data()        
        self.services.logger.info("Market data received %s" % (data))
        
        if self.x >= 0:
            self.services.logger.info("Sending Order Now:")
            o = Order()
            o.side = 1
            o.price = data[symbol]["ask-1"]["price"]
            o.size = 5000000
            o.leaves = o.size
            o.symbol = symbol
            o.id = "MyOrder"
            
            self.services.order_dispatcher.new_order(o)           
        
            self.x += 1
        print "!!!!!!!!!!!!!!!!!!! ", data["a"]["event"]
        if data["a"]["event"] == "trade":
            self.services.publisher.publish("DummyAgent", {"bid": data[symbol]["bid-0"]["price"], 
                                                           "ask": data[symbol]["ask-0"]["price"], 
                                                           "bid_size": data[symbol]["bid-0"]["size"], 
                                                           "ask_size": data[symbol]["ask-0"]["size"],
                                                           "price": data[symbol]["last"]["price"],
                                                           "quantity": data[symbol]["last"]["quantity"], 
                                                           "time":  data[symbol]["time"]})
        
    def process_report(self, id):
        execs = self.services.bus.get_executions()[id]
        self.services.logger.info("execution!!!!!!!!!!!!" + str(id)  + " number: " +  str(len(execs)))
        for e in execs:
            self.services.logger.info( e)
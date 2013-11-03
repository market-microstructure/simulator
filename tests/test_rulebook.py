'''
Created on Nov 2, 2013

@author: Silver
'''

from bus.Bus import Bus
from scheduler.ServiceLocator import ServiceLocator
from rulebook.Rulebook import Rulebook
from objects.Order import Order
from events.signals import Events
from numpy.ma.testutils import assert_equal
import numpy as np

def base_setup():
    services = ServiceLocator()
    services.bus = Bus()
    services.rulebook = Rulebook(services)
    services.events = Events
    return services

def setup_orderbook():
    services = base_setup()
    
    orderbook = {'a': {'ask-1': {'price': 65.549999999999997, 'size': 7000}, 
                       'ask-0': {'price': 65.450000000000003, 'size': 7250}, 
                       'ask-3': {'price': 65.75, 'size': 9000}, 
                       'ask-2': {'price': 65.650000000000006, 'size': 7000}, 
                       'ask-4': {'price': 65.849999999999994, 'size': 8400}, 
                       'bid-4': {'price': 64.950000000000003, 'size': 7000}, 
                       'bid-3': {'price': 65.049999999999997, 'size': 7000}, 
                       'bid-2': {'price': 65.150000000000006, 'size': 7000}, 
                       'bid-1': {'price': 65.25, 'size': 4000}, 
                       'bid-0': {'price': 65.349999999999994, 'size': 4000}, 
                       'last': {'price': 65.049999999999997, 'exchange': 'VIRTX', 'type': ' ', 'side': '?', 'quantity': 15383}, 
                       'stats': {'volume': 7401298, 'vwap': 65.147724209996682}, 
                       }}
    
    services.bus._public_data = orderbook
    return services
    
    
def basic_teardown():
    pass

def test_aggressive_buy_order_first_limit_1():
    services = setup_orderbook()
    
    #insert aggressive buy order
    o = Order()
    o.price = services.bus.get_market_data()['a']["ask-0"]["price"]
    o.size  = services.bus.get_market_data()['a']["ask-0"]["size"] / 2
    o.side = +1
    o.id = "order_test"
    o.symbol = "a"
    
    services.bus.get_orderbook()[o.id] = o
    
    services.rulebook.match_one(o.id)    
    assert services.bus.get_executions().has_key(o.id), "Rulebook generated no executions for id = %s, expected executions" % (o.id)
    assert len(services.bus.get_executions()[o.id]) == 1, "Number of executions need to be equal to one. Got: %d" % (len(services.bus.get_executions()[o.id]))
    assert services.bus.get_executions()[o.id][0].size == o.size, "Size of the execution must be equal to the size of the order : %d. Got %d instead" % (o.size, services.bus.get_executions()[o.id][0].size)
    assert services.bus.get_executions()[o.id][0].price == o.price, "Price of the execution must be equal to the size of the order : %f. Got %f instead" % (o.price, services.bus.get_executions()[o.id][0].price)
        
def test_aggressive_buy_order_first_limit_2():
    services = setup_orderbook()
    
    #insert aggressive buy order
    o = Order()
    o.price = services.bus.get_market_data()['a']["ask-0"]["price"]
    o.size  = services.bus.get_market_data()['a']["ask-0"]["size"] * 2
    o.side = +1
    o.id = "order_test"
    o.symbol = "a"
    
    services.bus.get_orderbook()[o.id] = o
    
    services.rulebook.match_one(o.id)    
    assert services.bus.get_executions().has_key(o.id), "Rulebook generated no executions for id = %s, expected executions" % (o.id)
    assert len(services.bus.get_executions()[o.id]) == 1, "Number of executions need to be equal to one. Got: %d" % (len(services.bus.get_executions()[o.id]))
    assert services.bus.get_executions()[o.id][0].size == services.bus.get_market_data()['a']["ask-0"]["size"], "Size of the execution must be equal to the size of the limit : %d. Got %d instead" % (services.bus.get_market_data()['a']["ask-0"]["size"], services.bus.get_executions()[o.id][0].size)
    assert services.bus.get_executions()[o.id][0].price == o.price, "Price of the execution must be equal to the size of the order : %f. Got %f instead" % (o.price, services.bus.get_executions()[o.id][0].price)

def test_aggressive_buy_order_second_limit_2():
    services = setup_orderbook()
    
    #insert aggressive buy order
    o = Order()
    o.price = services.bus.get_market_data()['a']["ask-1"]["price"]
    o.size  = services.bus.get_market_data()['a']["ask-1"]["size"] * 2 + services.bus.get_market_data()['a']["ask-0"]["size"]
    o.side = +1
    o.id = "order_test"
    o.symbol = "a"
    
    services.bus.get_orderbook()[o.id] = o
    
    services.rulebook.match_one(o.id)    
    
    assert services.bus.get_executions().has_key(o.id), "Rulebook generated no executions for id = %s, expected executions" % (o.id)
    assert_equal(len(services.bus.get_executions()[o.id]), 2, "Incorrect number of executions")
         
    assert_equal(services.bus.get_executions()[o.id][0].size, services.bus.get_market_data()['a']["ask-0"]["size"], "Size of the first execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][0].price, services.bus.get_market_data()['a']["ask-0"]["price"], "Price of first execution incorrect") 

    assert_equal(services.bus.get_executions()[o.id][1].size, services.bus.get_market_data()['a']["ask-1"]["size"], "Size of the second execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][1].price, services.bus.get_market_data()['a']["ask-1"]["price"], "Price of the second execution incorrect")
    
def test_aggressive_buy_order_second_limit_3():
    services = setup_orderbook()
    
    #insert aggressive buy order
    o = Order()
    o.price = services.bus.get_market_data()['a']["ask-1"]["price"]
    o.size  = services.bus.get_market_data()['a']["ask-1"]["size"] / 2 + services.bus.get_market_data()['a']["ask-0"]["size"]
    o.side = +1
    o.id = "order_test"
    o.symbol = "a"
    
    services.bus.get_orderbook()[o.id] = o
    
    services.rulebook.match_one(o.id)    
    
    assert services.bus.get_executions().has_key(o.id), "Rulebook generated no executions for id = %s, expected executions" % (o.id)
    assert_equal(len(services.bus.get_executions()[o.id]), 2, "Incorrect number of executions")
         
    assert_equal(services.bus.get_executions()[o.id][0].size, services.bus.get_market_data()['a']["ask-0"]["size"], "Size of the first execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][0].price, services.bus.get_market_data()['a']["ask-0"]["price"], "Price of first execution incorrect") 

    assert_equal(services.bus.get_executions()[o.id][1].size, services.bus.get_market_data()['a']["ask-1"]["size"] / 2, "Size of the second execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][1].price, services.bus.get_market_data()['a']["ask-1"]["price"], "Price of the second execution incorrect")

def test_aggressive_buy_order_second_limit_4():
    services = setup_orderbook()
    
    #insert aggressive buy order
    o = Order()
    o.price = services.bus.get_market_data()['a']["ask-1"]["price"]
    o.size  = services.bus.get_market_data()['a']["ask-0"]["size"] / 2 
    o.side = +1
    o.id = "order_test"
    o.symbol = "a"
    
    services.bus.get_orderbook()[o.id] = o
    
    services.rulebook.match_one(o.id)    
    
    assert services.bus.get_executions().has_key(o.id), "Rulebook generated no executions for id = %s, expected executions" % (o.id)
    assert_equal(len(services.bus.get_executions()[o.id]), 1, "Incorrect number of executions")
         
    assert_equal(services.bus.get_executions()[o.id][0].size, services.bus.get_market_data()['a']["ask-0"]["size"] / 2 , "Size of the first execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][0].price, services.bus.get_market_data()['a']["ask-0"]["price"], "Price of first execution incorrect") 

 
def test_aggressive_buy_order_second_limit_1():
    services = setup_orderbook()
    
    #insert aggressive buy order
    o = Order()
    o.price = services.bus.get_market_data()['a']["ask-1"]["price"]
    o.size  = services.bus.get_market_data()['a']["ask-1"]["size"] + services.bus.get_market_data()['a']["ask-0"]["size"]
    o.side = +1
    o.id = "order_test"
    o.symbol = "a"
    
    services.bus.get_orderbook()[o.id] = o
    
    services.rulebook.match_one(o.id)    
    
    assert services.bus.get_executions().has_key(o.id), "Rulebook generated no executions for id = %s, expected executions" % (o.id)
    assert_equal(len(services.bus.get_executions()[o.id]), 2, "Incorrect number of executions")
         
    assert_equal(services.bus.get_executions()[o.id][0].size, services.bus.get_market_data()['a']["ask-0"]["size"], "Size of the first execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][0].price, services.bus.get_market_data()['a']["ask-0"]["price"], "Price of first execution incorrect") 

    assert_equal(services.bus.get_executions()[o.id][1].size, services.bus.get_market_data()['a']["ask-1"]["size"], "Size of the second execution incorrect")
    assert_equal(services.bus.get_executions()[o.id][1].price, services.bus.get_market_data()['a']["ask-1"]["price"], "Price of the second execution incorrect")
    
if __name__ == "__main__":
    test_aggressive_buy_order_first_limit_1()

'''
Created on Sep 23, 2013

@author: Silver
'''

from ServiceLocator import ServiceLocator
from rulebook.Rulebook import Rulebook
from matching_engine.Level1MatchingEngine import Level1MatchingEngine
from injecter.Level1FastInjecter import Level1FastInjecter
from bus.Bus import Bus
from agent.DummyAgent import DummyAgent
from events.signals import Events
from tools.Order import *
import logging


if __name__ == "__main__":
    services = ServiceLocator()
    services.bus = Bus()
    services.matching_engine = Level1MatchingEngine(services)
    services.rulebook = Rulebook(services)
    services.injecter = Level1FastInjecter(services, "G:/st_sim/simulator/input_files/data.csv")
    services.events = Events
    services.order_dispatcher = OrderDispatcher(services)
    
    dummy = DummyAgent(services)
    
    # connect the market to the injecter events
    Events['SnapshotInject'].connect(services.matching_engine.on_inject)
    
    # connect the market to the agent events
    Events['ValidNewOrder'].connect(services.matching_engine.on_new_order)
    
    # connect the trader to the market events
    Events['MarketData'].connect(dummy.process)
    Events['Execution'].connect(dummy.process_report)
    
    # connect the injecter to the scheduler events
    Events['Start'].connect(services.injecter.main_loop)
    
    services.events["Start"].emit("simulation")
    
    
    
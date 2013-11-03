'''
Created on Sep 23, 2013

@author: Silver
'''

from ServiceLocator import ServiceLocator
from rulebook.Rulebook import Rulebook
from matching_engine.Level1MatchingEngine import Level1MatchingEngine
from injecter.Level1FastInjecter import Level1FastInjecter
from injecter.Level2HDFInjecter import Level2HDFInjecter
from bus.Bus import Bus
from agent.DummyAgent import DummyAgent
from events.signals import Events
from tools.Logger import *
from objects.Order import *
from datetime import datetime
from tools.Publisher import Publisher

if __name__ == "__main__":
    start = datetime.now()
    
    services = ServiceLocator()
    services.bus = Bus()
    services.matching_engine = Level1MatchingEngine(services)
    services.rulebook = Rulebook(services)
    services.injecter = Level2HDFInjecter(services, "G:/st_sim/simulator/input_files/test_trades.h5")
    services.events = Events
    services.order_dispatcher = OrderDispatcher(services)
    services.logger = get_logger()
    services.publisher = Publisher(services, "G:/st_sim/simulator/output_files")
    
    dummy = DummyAgent(services)
    
    # connect the market to the injecter events
    Events['SnapshotInject'].connect(services.matching_engine.on_inject)
    
    # connect the market to the agent events
    Events['ValidNewOrder'].connect(services.matching_engine.on_new_order)
    Events["AckNew"].connect(services.rulebook.match_one)
    
    # connect the trader to the market events
    Events['MarketData'].connect(dummy.process)
    #Events['MarketData'].connect(services.rulebook.match_all)
    Events['Execution'].connect(dummy.process_report)
    
    # connect the injecter to the scheduler events
    Events['Start'].connect(services.injecter.main_loop)
    Events['Stop'].connect(services.publisher.export)
    
    services.logger.info("starting the simulation")
    services.events["Start"].emit("simulation")
    services.events["Stop"].emit("simulation")
    
    end = datetime.now()
    print "Duration of simulation: ", start, end, end-start
    
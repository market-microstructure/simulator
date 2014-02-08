'''
Created on Feb 8, 2014

@author: Silver
'''

from ServiceLocator import ServiceLocator
from rulebook.ZIRulebook import ZIRulebook
from matching_engine.ZeroIntelligenceMatchingEngine import ZeroIntelligenceMatchingEngine

from injecter.ZIInjecter import ZIInjecter
from bus.ZIBus import ZIBus
from agent.SORAgent import SORAgent
from events.signals import Events
from tools.Logger import *
from objects.Order import *
from datetime import datetime
from tools.Publisher import Publisher
from agent.ZeroIntelligenceAgent import ZeroIntelligenceAgent
from objects.AgentFactory import AgentFactory


if __name__ == "__main__":
    start = datetime.now()
    
    services = ServiceLocator()
    services.bus = ZIBus()
    services.matching_engine = ZeroIntelligenceMatchingEngine(services)
    services.rulebook = ZIRulebook(services)
    services.injecter = ZIInjecter(services, "G:/st_sim/simulator/input_files/test_trades.h5")
    services.events = Events
    services.order_dispatcher = OrderDispatcher(services)
    services.logger = get_logger()
    services.publisher = Publisher(services, "G:/st_sim/simulator/output_files")
    services.factory = AgentFactory(services)
    
    zi = ZeroIntelligenceAgent(services, "ZIAgent")
    sor = SORAgent(services, "SOR")
    
    # connect the market to the injecter events
    Events['SnapshotInject'].connect(services.matching_engine.on_inject)
    
    # connect the market to the agent events
    Events['ValidNewOrder'].connect(services.matching_engine.on_new_order)
    Events["AckNew"].connect(services.rulebook.match_one)
          
    # connect the trader to the market events
    Events['MarketData'].connect(zi.process)
    Events['MarketData'].connect(sor.process)
    #Events['MarketData'].connect(services.rulebook.match_all)
    #Events['Execution'].connect(zi.process_report)
    #Events['Execution'].connect(sor.process_report)
    services.factory.add_agent("ZIAgent", zi)
    services.factory.add_agent("SOR", sor)
    Events["Execution"].connect(services.factory.process_report)
    Events["Reject"].connect(services.factory.process_reject)
    
        
    # connect the injecter to the scheduler events
    Events['Start'].connect(services.injecter.main_loop)
    Events['Stop'].connect(services.publisher.export)
    
    services.logger.info("starting the simulation")
    services.events["Start"].emit("simulation")
    services.events["Stop"].emit("simulation")
    
    end = datetime.now()
    print "Duration of simulation: ", start, end, end-start
    
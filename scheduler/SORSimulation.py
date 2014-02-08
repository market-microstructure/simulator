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
import pandas as pd
from Simulation import Simulation

class SORSimulation(Simulation):
    def __init__(self, parameters):
        if not parameters.has_key("agent"): logging.warning("SORSimulation requires class of agent as a parameter")            
        if not parameters.has_key("agent-parameters"): logging.warning("SORSimulation requires agent parameter dictionary as an input (e.g. {'size': 50, 'price': 102, 'side': 'Buy', 'id': 'my_agent_001'})")
        
        self.services = ServiceLocator()
        self.services.simulation["id"] = "SORSimulation_%s" % datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S%f")
        self.services.simulation["output-path"] = parameters["output-path"] if parameters.has_key("output-path") else "../output_files"
        self.services.simulation["input-path"] = parameters["input-path"] if parameters.has_key("input-path") else "../input_files"
        self.services.bus = ZIBus()
        self.services.matching_engine = ZeroIntelligenceMatchingEngine(self.services)
        self.services.rulebook = ZIRulebook(self.services)
        self.services.injecter = ZIInjecter(self.services, "")
        self.services.events = Events
        self.services.order_dispatcher = OrderDispatcher(self.services)
        self.services.logger = get_logger()
        self.services.publisher = Publisher(self.services, self.services.simulation["output-path"])
        self.services.factory = AgentFactory(self.services)
        
        
        zi = ZeroIntelligenceAgent(self.services, {"id": "ZIAgent", "nb_lit_venues": 4, "nb_dark_venues": 0})
        if parameters.has_key("agent"):
            Agent = parameters["agent"]
            params = parameters["agent-parameters"] if parameters.has_key("agent-parameters") else {"id": "DefaultAgent"}            
            sor = Agent(self.services, params)
        
        # connect the market to the injecter events
        self.services.events['SnapshotInject'].connect(self.services.matching_engine.on_inject)
        
        # connect the market to the agent events
        self.services.events['ValidNewOrder'].connect(self.services.matching_engine.on_new_order)
        self.services.events["AckNew"].connect(self.services.rulebook.match_one)
              
        # connect the trader to the market events
        self.services.events['MarketData'].connect(zi.process)
        self.services.events['MarketData'].connect(sor.process)
        
        #Events['Execution'].connect(zi.process_report)
        #Events['Execution'].connect(sor.process_report)
        self.services.factory.add_agent("ZIAgent", zi)
        self.services.factory.add_agent(params["id"], sor)
        
        self.services.events["Execution"].connect(self.services.factory.process_report)
        self.services.events["Reject"].connect(self.services.factory.process_reject)       
            
        # connect the injecter to the scheduler events
        self.services.events['Start'].connect(self.services.injecter.main_loop)
        self.services.events['Stop'].connect(self.services.publisher.export)
        
        
    def run(self):
        start = datetime.now()
        self.services.logger.info("starting the simulation")
        self.services.events["Start"].emit("simulation")
        self.services.events["Stop"].emit("simulation")
        
        end = datetime.now()
        self.services.logger.info("Duration of simulation. Start: %s. End: %s. Duration: %s" % (start, end, end-start))
        
    def get_results(self):
        df = pd.read_csv(self.services.simulation["output-path"]+"/"+self.services.simulation["id"] + ".csv", sep = ';')
        return df
        
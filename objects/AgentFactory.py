'''
Created on Feb 8, 2014

@author: Silver
'''

class AgentFactory():
    def __init__(self, service_locator):
        self.services = service_locator
        self.agents = {}
        
    def add_agent(self, agent_id, agent):
        self.agents[agent_id] = agent
    
    def process_report(self, order_id):
        parent = self.services.bus.get_executions()[order_id][0].parent
        self.agents[parent].process_report(order_id)
        
    def process_reject(self, order_id):
        parent = self.services.bus.get_rejects()[order_id].parent
        self.agents[parent].process_reject(order_id)
        
'''
Created on Feb 8, 2014

@author: Silver
'''

from SORSimulation import SORSimulation
from agent.SORAgent import SORAgent

if __name__ == "__main__":
    sim = SORSimulation({"agent": SORAgent, "agent-parameters": {'size': 5000, 'price': 102, 'side': 'buy', 'id': 'my_sor_agent_001'}})
    sim.run()
    df = sim.get_results()
    print df
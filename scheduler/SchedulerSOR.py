'''
Created on Feb 8, 2014

@author: Silver
'''

from SORSimulation import SORSimulation
from agent.SORAgent import SORAgent

if __name__ == "__main__":
    parameters = {"agent": SORAgent, "agent-parameters": {"side": "Sell", "size": 150, "price": 100, "id": "my_agent_01"}}
    sim = SORSimulation(parameters)
    sim.run()
    df = sim.get_results()
    print df
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from pprint import pprint

pprint(HfApiModel().model_id)


model = HfApiModel()
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)


agent.run("How long does it take to get to the moon with a Sturn 5 rocket?")

agent.run("What's the code to generate fibonacci numbers?")
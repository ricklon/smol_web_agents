from smolagents import CodeAgent, HfApiModel
from pprint import pprint

pprint(HfApiModel().model_id)


model = HfApiModel()
agent = CodeAgent(tools=[], model=model, add_base_tools=True)


agent.run("Review the page source and say what forms are on the page? http://localhost:5174 ")
agent.run("Does the page have a button with the words 'Login Form'? http://localhost:5174 ")
agent.run("What words does this page have? http://localhost:5174 ")


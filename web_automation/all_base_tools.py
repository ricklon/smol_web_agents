from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from pprint import pprint

pprint(HfApiModel().model_id)


model = HfApiModel()
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model, add_base_tools=True)


agent.run("Generate a pink and blue smiley face. If you don't have image generation say so.")

agent.run(""""
    I'd like you to help me with a research task. Please:
    1. Search for the latest news about quantum computing breakthroughs
    2. Create a brief summary of the top 3 findings
    3. Generate a simple visualization showing the timeline of these breakthroughs
    4. Save the summary and any code you write to a file called "quantum_computing_report.txt"

    If you have access to image generation, please also create an artistic representation of a quantum computer."
    """)
#
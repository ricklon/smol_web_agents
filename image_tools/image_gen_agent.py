from smolagents import CodeAgent, HfApiModel, load_tool
from pprint import pprint


model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

agent = CodeAgent(tools=[image_generation_tool], model=model)

image = agent.run(
    "Improve this prompt, then generate an image of it.", additional_args={'user_prompt': 'A rabbit wearing a space suit'}
)

pprint(image)





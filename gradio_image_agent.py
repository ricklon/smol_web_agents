from smolagents import (
    load_tool,
    CodeAgent,
    HfApiModel,
    GradioUI
)

model_id = "Qwen/Qwen2.5-Coder-32B-Instruct"


# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

model = HfApiModel(model_id=model_id)

# Initialize the agent with the image generation tool
agent = CodeAgent(tools=[image_generation_tool], model=model)

GradioUI(agent).launch()

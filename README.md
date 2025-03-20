# SMOLagents Tools Documentation

This document provides an overview of the available tools in the SMOLagents framework and how to use them.

## Default Toolbox

When initializing an agent with `add_base_tools=True`, the following tools are automatically added:

| Tool | Description | Import |
|------|-------------|--------|
| **DuckDuckGoSearchTool** | Performs web searches using DuckDuckGo | `from smolagents import DuckDuckGoSearchTool` |
| **TranscriberTool** | Transcribes audio to text using Whisper-Turbo | `from smolagents import TranscriberTool` |
| **BashTool** | Executes shell commands | `from smolagents import BashTool` |
| **FileReadTool** | Reads content from files | `from smolagents import FileReadTool` |
| **FileWriteTool** | Writes content to files | `from smolagents import FileWriteTool` |
| **PythonInterpreterTool** | Executes Python code (only added to ToolCallingAgent) | `from smolagents import PythonInterpreterTool` |
| **MlxInterpreterTool** | For machine learning with MLX (only if MLX is installed) | `from smolagents import MlxInterpreterTool` |

**Note**: For `CodeAgent`, `PythonInterpreterTool` is not added since it already has built-in code execution capability.

## Basic Example

```python
from smolagents import CodeAgent, HfApiModel

# Initialize model
model = HfApiModel()  # Uses default free model

# Create agent with default tools
agent = CodeAgent(
    tools=[],  # No additional tools
    model=model,
    add_base_tools=True  # Add all default tools
)

# Run the agent
result = agent.run(
    "Search for information about quantum computing and save a summary to a file."
)
```

## Using Individual Tools

You can use the tools directly without creating an agent:

```python
from smolagents import DuckDuckGoSearchTool

# Initialize the tool
search_tool = DuckDuckGoSearchTool()

# Use the tool
results = search_tool("Current developments in quantum computing")
print(results)
```

## Creating Custom Tools

Create your own tool using the `@tool` decorator:

```python
from smolagents import tool

@tool
def my_custom_tool(input_param: str) -> str:
    """
    Description of what this tool does.
    
    Args:
        input_param: Description of the input parameter.
    """
    # Tool implementation
    result = input_param.upper()  # Just an example
    return result
```

## Loading Tools from Hub

You can load community-created tools from the Hugging Face Hub:

```python
from smolagents import load_tool, CodeAgent, HfApiModel

# Load a tool from the Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

# Create an agent with the loaded tool
model = HfApiModel()
agent = CodeAgent(tools=[image_generation_tool], model=model)

# Run the agent
agent.run("Generate an image of a cat in space")
```

## Image Generation Example

Here's a complete example of an image generation agent:

```python
from smolagents import CodeAgent, HfApiModel, load_tool

# Load image generation tool
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

# Initialize the model
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

# Create the agent
agent = CodeAgent(tools=[image_generation_tool], model=model)

# Run the agent
result = agent.run(
    "Improve this prompt, then generate an image of it.", 
    additional_args={'user_prompt': 'A rabbit wearing a space suit'}
)
```

## Demos

This repository contains several demo scripts showcasing different SMOLagents capabilities:

| Demo | Learning Objective |
|------|-------------------|
| **basic_agent.py** | Create a simple CodeAgent with web search capabilities |
| **basic_fetch.py** | Run multiple queries through an agent and format the output |
| **basic_web_agent.py** | Build a custom agent for web browsing with navigation methods |
| **gradio_image_agent.py** | Integrate image generation tools with a Gradio UI |
| **helium_test.py** | Configure Chrome browser with specific options for web automation |
| **image_gen_agent.py** | Use text-to-image generation tools with prompt improvement |
| **image_save_tool.py** | Create custom tools to save images and combine with other tools |
| **web_browser.py** | Build robust web automation with callbacks and error handling |
| **what_forms_are_on_page.py** | Analyze web page structure and content programmatically |
| **all_base_tools.py** | Use all base tools for complex research and generation tasks |

## Form Analyzer Demo

The Form Analyzer is a specialized tool for web form analysis and automation. It automatically detects forms on web pages, extracts their structure, and generates scripts to interact with them.

```python
from form_analyzer import FormAnalyzer

# Initialize analyzer
analyzer = FormAnalyzer(headless=False)  # Set headless=True for no UI

# Analyze a page with forms
result = analyzer.analyze_page("http://localhost:5174")

# Save results to JSON and generate interaction script
analyzer.save_result(result, "form_analyzer_output/form_analysis.json")
script = analyzer.generate_helium_script(result)
with open("form_analyzer_output/form_interaction.py", "w") as f:
    f.write(script)
```

### Key Features

- **Automatic Form Detection**: Identifies all forms on a web page
- **Field Analysis**: Extracts details about form fields (type, label, required status, options)
- **Screenshot Capture**: Takes screenshots of each form for visual verification
- **Code Generation**: Automatically creates Helium scripts for form automation
- **AI Integration**: Works with SMOLagents for intelligent form testing

For more details, see the [Form Analyzer documentation](form_analyzer_readme.md).

## Resources

- [SMOLagents GitHub Repository](https://github.com/huggingface/smolagents)
- [Default Tools Source](https://github.com/huggingface/smolagents/blob/v1.11.0/src/smolagents/default_tools.py)
- [Tool Implementation Source](https://github.com/huggingface/smolagents/blob/v1.11.0/src/smolagents/tools.py)

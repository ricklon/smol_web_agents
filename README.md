# SMOLagents Web Tools

This repository provides a collection of tools and examples for building small, efficient web agents with Python.

## Project Organization

The project is organized into the following categories:

### Web Automation
Tools for automating browser interactions and web navigation:
- `web_browser.py` - Core web browser automation
- `basic_web_agent.py` - Simple web agent implementation
- `basic_agent.py` - Core agent functionality
- `helium_test.py` - Browser automation tests
- `all_base_tools.py` - Utility tools for agents
- `basic_fetch.py` - Basic web content fetching

### Form Tools
Specialized tools for analyzing and interacting with web forms:
- `form_analyzer.py` - Analyzes and extracts form fields
- `form_review.py` - Reviews and validates forms
- `what_forms_are_on_page.py` - Detects forms on web pages
- `form_analyzer_output/form_interaction.py` - Generated form interaction scripts

### Image Tools
Tools for working with images and visual content:
- `image_to_text_tool.py` - Converts images to text using SmolVLM2
- `image_save_tool.py` - Saves and manipulates images
- `image_gen_agent.py` - Text-to-image generation with prompt enhancement

### Basic Examples
Simple examples to understand core functionality:
- `demo_image_to_text.py` - Simple demonstration of image-to-text conversion
- `basic_fetch.py` - Example of fetching web content

### UI Examples
Examples with user interfaces:
- `gradio_image_agent.py` - Gradio interface for image generation agent
- `gradio_image_to_text.py` - Gradio UI for image-to-text processing

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

## Getting Started

1. Install dependencies with `uv pip install -e .`
2. Sync dependencies with `uv sync`
3. Start with basic examples to understand core functionality
4. Progress to more complex web automation and form analysis tools

## Development

- **Lint Code**: `ruff check .`
- **Type Check**: `mypy .`
- **Format Code**: `ruff format .`

## Demo Examples

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

For more details, see the [Form Analyzer documentation](form_analyzer_readme.md).

## Requirements

- Python 3.12+
- Primary dependencies: smolagents, selenium, helium, pillow

## Resources

- [SMOLagents GitHub Repository](https://github.com/huggingface/smolagents)
- [Default Tools Source](https://github.com/huggingface/smolagents/blob/v1.11.0/src/smolagents/default_tools.py)
- [Tool Implementation Source](https://github.com/huggingface/smolagents/blob/v1.11.0/src/smolagents/tools.py)
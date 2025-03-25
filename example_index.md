# SMOLagents Web Tools Examples Index

This index provides a guide to all examples in the repository, organized by functionality and complexity level.

## Examples by Category

### Web Automation
| Example | Description | Complexity | Tags |
|---------|-------------|------------|------|
| `web_automation/basic_web_agent.py` | Simple web browsing agent | Beginner | #web #agent |
| `web_automation/web_browser.py` | Core browser automation with advanced error handling | Intermediate | #web #browser #error-handling |
| `web_automation/helium_test.py` | Chrome browser configuration for automation | Beginner | #web #browser #configuration |
| `web_automation/basic_agent.py` | Simple CodeAgent with web search capabilities | Beginner | #agent #search |
| `web_automation/basic_fetch.py` | Running multiple queries through an agent | Beginner | #agent #search #multi-query |
| `web_automation/all_base_tools.py` | Usage of all base tools for complex tasks | Advanced | #tools #integration |

### Form Analysis and Interaction
| Example | Description | Complexity | Tags |
|---------|-------------|------------|------|
| `form_tools/form_analyzer.py` | Tool to identify and extract form fields | Intermediate | #form #analysis |
| `form_tools/form_review.py` | Review and analysis of form data | Intermediate | #form #validation |
| `form_tools/what_forms_are_on_page.py` | Web page structure analysis | Beginner | #form #detection |
| `form_tools/form_analyzer_output/form_interaction.py` | Generated script for form interaction | Intermediate | #form #automation |

### Image Processing
| Example | Description | Complexity | Tags |
|---------|-------------|------------|------|
| `image_tools/image_to_text_tool.py` | Custom tool for image-to-text processing | Intermediate | #image #text #vision |
| `image_tools/image_save_tool.py` | Tool for saving and manipulating images | Beginner | #image #storage |
| `image_tools/image_gen_agent.py` | Text-to-image generation with prompt improvement | Advanced | #image #generation |

### Basic Examples
| Example | Description | Complexity | Tags |
|---------|-------------|------------|------|
| `basic_examples/demo_image_to_text.py` | Demonstration of image-to-text capabilities | Beginner | #image #text #demo |

### UI Examples
| Example | Description | Complexity | Tags |
|---------|-------------|------------|------|
| `ui_examples/gradio_image_agent.py` | Gradio UI for image generation agent | Intermediate | #image #generation #ui |
| `ui_examples/gradio_image_to_text.py` | Gradio UI for image-to-text processing | Intermediate | #image #text #ui |

## Examples by Complexity Level

### Beginner Level
- `web_automation/basic_web_agent.py` - First steps with web automation
- `web_automation/helium_test.py` - Setting up and configuring browsers
- `web_automation/basic_agent.py` - Introduction to agent capabilities
- `web_automation/basic_fetch.py` - Basic web content retrieval
- `form_tools/what_forms_are_on_page.py` - Simple form detection
- `image_tools/image_save_tool.py` - Basic image handling
- `basic_examples/demo_image_to_text.py` - Simple image analysis

### Intermediate Level
- `web_automation/web_browser.py` - Advanced browser control
- `form_tools/form_analyzer.py` - Comprehensive form analysis 
- `form_tools/form_review.py` - Form validation techniques
- `form_tools/form_analyzer_output/form_interaction.py` - Automated form interactions
- `image_tools/image_to_text_tool.py` - Vision-language processing
- `ui_examples/gradio_image_agent.py` - Building UI-based agents
- `ui_examples/gradio_image_to_text.py` - UI for vision tasks

### Advanced Level
- `web_automation/all_base_tools.py` - Complex tool integration
- `image_tools/image_gen_agent.py` - Advanced generative AI techniques

## Learning Pathways

### Web Automation Path
1. Start with `web_automation/basic_agent.py` to understand core agent concepts
2. Move to `web_automation/basic_web_agent.py` for web browsing capabilities
3. Explore `web_automation/web_browser.py` for advanced browser manipulation
4. Learn configuration with `web_automation/helium_test.py`
5. Master complex scenarios with `web_automation/all_base_tools.py`

### Form Analysis Path
1. Begin with `form_tools/what_forms_are_on_page.py` for basic form detection
2. Progress to `form_tools/form_analyzer.py` for detailed form extraction
3. Add validation with `form_tools/form_review.py`
4. Automate with `form_tools/form_analyzer_output/form_interaction.py`

### Image Processing Path
1. Start with `basic_examples/demo_image_to_text.py` for core concepts
2. Learn image handling with `image_tools/image_save_tool.py`
3. Explore visual understanding with `image_tools/image_to_text_tool.py`
4. Add UI with `ui_examples/gradio_image_to_text.py`
5. Master generative AI with `image_tools/image_gen_agent.py`

## Prerequisites

Different examples may require different prerequisites. Here's a general guide:

- **All examples**: Python 3.12+, smolagents package
- **Web automation**: selenium, helium, ChromeDriver
- **Image processing**: pillow, SmolVLM2
- **UI examples**: gradio
- **Form tools**: selenium, helium, ChromeDriver
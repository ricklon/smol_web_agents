"""
Gradio UI for Image-to-Text Agent using SmolVLM2-2.2B-Instruct

This script creates a web interface for the image-to-text functionality using:
1. The SmolVLM2-2.2B-Instruct model
2. smolagents for agent capabilities
3. Gradio for the web UI
"""

import os
import sys
from typing import Dict, Any, Optional, Union, List

# Import smolagents components
from smolagents import (
    CodeAgent,
    HfApiModel,
    GradioUI
)

# Add the path to the image_to_text_tool.py file
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import our custom tools
from image_to_text_tool import image_to_text, ocr_image, analyze_image

def main():
    """Initialize and launch the Gradio interface for the image-to-text agent"""
    
    # Set the model ID for the agent's language model
    # You can use various models based on your requirements
    model_id = "meta-llama/Llama-3.3-70B-Instruct"  # Default choice
    
    # Alternatively, you can use a smaller model if resources are limited:
    # model_id = "google/gemma-1.1-7b-it"
    
    print(f"Initializing agent with model: {model_id}")
    
    # Initialize the language model for the agent
    model = HfApiModel(model_id=model_id)
    
    # Initialize the agent with the image processing tools
    agent = CodeAgent(
        tools=[image_to_text, ocr_image, analyze_image],
        model=model,
        add_base_tools=True,  # Include other useful tools
        max_steps=10  # Limit the number of steps for safety
    )
    
    # Configure the Gradio UI with helpful usage instructions
    ui = GradioUI(
        agent,
        title="Image-to-Text Analysis Tool",
        description="""
        ## SmolVLM2 Image-to-Text Analysis
        
        Upload an image and ask questions about it, extract text from it, or get detailed descriptions.
        
        ### Example prompts:
        - "Describe this image in detail"
        - "Extract all text visible in this image"
        - "What objects can you see in this picture?"
        - "Is there a person in this image? What are they doing?"
        - "What colors are most prominent in this image?"
        
        ### How to use:
        1. Upload an image using the file uploader
        2. Type your prompt or question
        3. Click "Submit" and wait for the response
        
        The model will process your image and provide a textual response based on your query.
        """
    )
    
    # Launch the Gradio interface
    # You can set share=True to get a public link
    ui.launch(share=False)

if __name__ == "__main__":
    main()

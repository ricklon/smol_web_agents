"""
Demo Script for Image-to-Text Tool using SmolVLM2-2.2B-Instruct

This script demonstrates how to use the image-to-text tool directly with examples.
"""

import os
import sys
import argparse
from pprint import pprint

# Add the path to the image_to_text_tool.py file
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import our tool and agent creator
from image_to_text_tool import (
    get_model_instance,
    image_to_text,
    ocr_image, 
    analyze_image,
    create_image_to_text_agent
)

def demo_direct_tool_usage(image_path):
    """
    Demonstrate direct usage of the tools without an agent
    
    Args:
        image_path: Path to an image file
    """
    print("\n" + "="*60)
    print(" Direct Tool Usage Demo ".center(60, "="))
    print("="*60)
    
    # Make sure the model is loaded
    print("\nLoading model (this may take a moment)...")
    model = get_model_instance()
    
    print("\n1. Basic Image Description")
    print("-" * 30)
    description = image_to_text(
        image=image_path,
        prompt="Describe this image in detail",
        max_tokens=150
    )
    print(description)
    
    print("\n2. OCR Text Extraction")
    print("-" * 30)
    extracted_text = ocr_image(image_path)
    print(extracted_text)
    
    print("\n3. Specific Image Analysis")
    print("-" * 30)
    analysis = analyze_image(
        image=image_path,
        question="What colors are most prominent in this image?"
    )
    print(analysis)
    
    return description, extracted_text, analysis

def demo_agent_usage(image_path):
    """
    Demonstrate using the tools via an agent
    
    Args:
        image_path: Path to an image file
    """
    print("\n" + "="*60)
    print(" Agent-Based Usage Demo ".center(60, "="))
    print("="*60)
    
    # Create the agent (using a smaller model for faster demos)
    print("\nInitializing agent (this may take a moment)...")
    agent = create_image_to_text_agent(model_id="google/gemma-1.1-7b-it")
    
    # Prepare and run different example prompts
    prompts = [
        f"Describe what's in this image: {image_path}",
        f"Extract any text from this image: {image_path}",
        f"What's the dominant color in this image: {image_path}"
    ]
    
    responses = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{i}. Running prompt: {prompt}")
        print("-" * 30)
        
        response = agent.run(prompt)
        responses.append(response)
        
        print(response)
    
    return responses

def main():
    """Main function to run the demo"""
    parser = argparse.ArgumentParser(description="Demo for Image-to-Text Tool")
    parser.add_argument("--image", type=str, help="Path to an image file", required=False)
    args = parser.parse_args()
    
    # Set a default image if none provided
    image_path = args.image
    
    if not image_path:
        # Check if any images exist in the current directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        for file in os.listdir('.'):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_path = file
                print(f"Using found image: {image_path}")
                break
                
        # If still no image, provide instructions
        if not image_path:
            print("No image provided and no images found in the current directory.")
            print("Please specify an image path using --image or place an image in the current directory.")
            return
    
    # Verify the image exists
    if not os.path.exists(image_path):
        print(f"Error: Image path not found: {image_path}")
        return
    
    # Run the direct tool usage demo
    direct_results = demo_direct_tool_usage(image_path)
    
    # Run the agent-based demo
    agent_results = demo_agent_usage(image_path)
    
    print("\n" + "="*60)
    print(" Demo Complete ".center(60, "="))
    print("="*60)
    
    print("\nYou can now use these tools in your own applications!")
    print("Check the 'image_to_text_tool.py' file for more details on available functions.")

if __name__ == "__main__":
    main()

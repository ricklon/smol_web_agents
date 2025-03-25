"""
Image-to-Text Tool using SmolVLM2-2.2B-Instruct

This script creates a custom tool for smolagents that can:
1. Process images using SmolVLM2-2.2B-Instruct
2. Generate text descriptions, captions, or transcriptions
3. Answer questions about image content
"""

import os
import base64
import torch
from io import BytesIO
from PIL import Image
from urllib.request import urlopen
from typing import Dict, Any, Optional, Union, List

# Import smolagents components
from smolagents import tool, CodeAgent, HfApiModel

# Check if transformers is installed, install if needed
try:
    from transformers import AutoProcessor, AutoModelForImageTextToText
except ImportError:
    import subprocess
    print("Installing required packages...")
    subprocess.check_call(["pip", "install", "transformers"])
    from transformers import AutoProcessor, AutoModelForImageTextToText

class SmolVLMImageToText:
    """Class to manage SmolVLM2 model for image-to-text processing"""
    
    def __init__(self, model_path="HuggingFaceTB/SmolVLM2-2.2B-Instruct", device=None):
        """
        Initialize the SmolVLM2 model
        
        Args:
            model_path: HuggingFace model path
            device: Device to run the model on (cuda, cpu, etc.)
        """
        self.model_path = model_path
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Loading SmolVLM2 model from {model_path} on {self.device}...")
        
        # Load processor and model
        self.processor = AutoProcessor.from_pretrained(model_path)
        
        # Load the model with appropriate settings
        dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        attn_implementation = "flash_attention_2" if self.device == "cuda" else "eager"
        
        try:
            self.model = AutoModelForImageTextToText.from_pretrained(
                model_path, 
                torch_dtype=dtype,
                _attn_implementation=attn_implementation
            ).to(self.device)
        except Exception as e:
            # Fallback without flash attention if it fails
            print(f"Failed to load with flash attention: {e}")
            print("Falling back to standard attention...")
            self.model = AutoModelForImageTextToText.from_pretrained(
                model_path, 
                torch_dtype=dtype
            ).to(self.device)
            
        print("Model loaded successfully!")
    
    def _load_image(self, image_source: Union[str, bytes, Image.Image]) -> Image.Image:
        """
        Load an image from various sources
        
        Args:
            image_source: Can be a file path, URL, base64 string, bytes, or PIL Image
            
        Returns:
            PIL Image object
        """
        if isinstance(image_source, Image.Image):
            return image_source
            
        if isinstance(image_source, str):
            # Check if it's a URL
            if image_source.startswith(("http://", "https://")):
                with urlopen(image_source) as response:
                    return Image.open(BytesIO(response.read()))
            
            # Check if it's a base64 string
            if "base64," in image_source:
                image_source = image_source.split("base64,")[1]
                
            try:
                # Try to decode as base64
                image_bytes = base64.b64decode(image_source)
                return Image.open(BytesIO(image_bytes))
            except:
                # Assume it's a file path
                return Image.open(image_source)
                
        if isinstance(image_source, bytes):
            return Image.open(BytesIO(image_source))
            
        raise ValueError("Unsupported image source format")
    
    def process_image(self, 
                      image: Union[str, bytes, Image.Image], 
                      prompt: str = "Describe this image in detail", 
                      max_new_tokens: int = 512,
                      do_sample: bool = True,
                      temperature: float = 0.7) -> str:
        """
        Process an image and generate text based on the prompt
        
        Args:
            image: The image to process (file path, URL, base64, bytes, or PIL Image)
            prompt: The text prompt to guide the model
            max_new_tokens: Maximum number of tokens to generate
            do_sample: Whether to use sampling for generation
            temperature: Temperature for sampling (higher = more random)
            
        Returns:
            Generated text response
        """
        # Load the image
        pil_image = self._load_image(image)
        
        # Prepare inputs using chat template
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": pil_image},
                ],
            },
        ]
        
        # Process the inputs
        inputs = self.processor.apply_chat_template(
            messages, 
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)
        
        # Generate output
        generated_ids = self.model.generate(
            **inputs,
            do_sample=do_sample,
            temperature=temperature,
            max_new_tokens=max_new_tokens
        )
        
        # Decode the generated text
        generated_text = self.processor.batch_decode(
            generated_ids, 
            skip_special_tokens=True
        )[0]
        
        return generated_text

# Create a singleton instance of the model
_model_instance = None

def get_model_instance(model_path="HuggingFaceTB/SmolVLM2-2.2B-Instruct", device=None):
    """Get or create the model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = SmolVLMImageToText(model_path, device)
    return _model_instance

@tool
def image_to_text(
    image: str, 
    prompt: str = "Describe this image in detail",
    max_tokens: int = 512,
    temperature: float = 0.7
) -> str:
    """
    Converts an image to text using SmolVLM2 model.
    
    Args:
        image: The image file path, URL, or base64-encoded string
        prompt: The text prompt to guide the model
        max_tokens: Maximum number of tokens to generate
        temperature: Temperature for text generation (higher = more random)
        
    Returns:
        Generated text description of the image
    """
    model = get_model_instance()
    return model.process_image(
        image=image,
        prompt=prompt,
        max_new_tokens=max_tokens,
        temperature=temperature
    )

@tool
def ocr_image(image: str) -> str:
    """
    Performs OCR (Optical Character Recognition) on an image to extract text.
    
    Args:
        image: The image file path, URL, or base64-encoded string
        
    Returns:
        Extracted text from the image
    """
    model = get_model_instance()
    return model.process_image(
        image=image,
        prompt="What text is visible in this image? Extract and transcribe all text content.",
        max_new_tokens=256,
        temperature=0.3  # Lower temperature for more deterministic OCR results
    )

@tool
def analyze_image(image: str, question: str) -> str:
    """
    Analyzes an image and answers a specific question about it.
    
    Args:
        image: The image file path, URL, or base64-encoded string
        question: The specific question to answer about the image
        
    Returns:
        Answer to the question about the image
    """
    model = get_model_instance()
    return model.process_image(
        image=image,
        prompt=question,
        max_new_tokens=512,
        temperature=0.5
    )

# Create a demo agent that can use these tools
def create_image_to_text_agent(model_id="meta-llama/Llama-3.3-70B-Instruct"):
    """
    Creates an agent that can perform image-to-text tasks.
    
    Args:
        model_id: The model ID to use for the agent
        
    Returns:
        CodeAgent: The configured agent
    """
    # Initialize the model
    model = HfApiModel(model_id=model_id)
    
    # Create the agent with our tools
    agent = CodeAgent(
        tools=[image_to_text, ocr_image, analyze_image],
        model=model,
        add_base_tools=True
    )
    
    return agent

# Example usage
if __name__ == "__main__":
    # Create the agent
    agent = create_image_to_text_agent()
    
    # Example prompts
    example_prompts = [
        "Describe what's in this image: path/to/image.jpg",
        "Extract all text from this image: https://example.com/image.png",
        "Is there a person in this image? path/to/portrait.jpg",
        "What color is the dominant object in this image? path/to/image.jpg"
    ]
    
    print("Image-to-Text Agent is ready!")
    print("Example prompts you could try:")
    for prompt in example_prompts:
        print(f"- {prompt}")
    
    # You can run the agent with a prompt
    # result = agent.run("Describe what's in this image: path/to/your/image.jpg")
    # print(result)

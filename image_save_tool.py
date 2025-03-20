from smolagents import CodeAgent, HfApiModel, load_tool, tool
import base64
from PIL import Image
import io

@tool
def save_image(image_data: str, output_path: str) -> str:
    """
    Saves an image to the specified output path. The image_data can be either a base64 encoded string
    or a PIL Image object.
    
    Args:
        image_data: The image to save, either as a base64 encoded string or a PIL Image object.
        output_path: The file path where the image should be saved.
    """
    try:
        # Check if image_data is a base64 string
        if isinstance(image_data, str):
            # Try to decode base64 data
            try:
                # Remove potential header from base64 string if present
                if "base64," in image_data:
                    image_data = image_data.split("base64,")[1]
                
                # Decode base64 string
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            except Exception as e:
                return f"Failed to decode base64 image data: {str(e)}"
        elif hasattr(image_data, 'save'):  # Check if it's a PIL Image
            image = image_data
        else:
            return "Unsupported image data format. Please provide a base64 string or PIL Image."
        
        # Save the image
        image.save(output_path)
        return f"Image successfully saved to {output_path}"
    
    except Exception as e:
        return f"Error saving image: {str(e)}"

# Load the image generation tool
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

# Initialize the model
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")  # You can use your preferred model

# Create the agent with both tools
agent = CodeAgent(
    tools=[image_generation_tool, save_image],
    model=model,
    add_base_tools=True  # Add other useful tools
)

# Run the agent
if __name__ == "__main__":
    result = agent.run(
        """Please perform the following tasks:
        1. Generate an image of a futuristic cityscape with flying cars
        2. Improve the image quality if possible
        3. Save the final image to 'futuristic_city.png'
        """
    )
    
    print(result)

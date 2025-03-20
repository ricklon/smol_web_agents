# -*- coding: utf-8 -*-
"""web_browser module

Adapted from: https://github.com/huggingface/notebooks/blob/main/smolagents_doc/en/pytorch/web_browser.ipynb
"""

from io import BytesIO
from time import sleep
import os

# Third-party imports
import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Local imports
from smolagents import CodeAgent, HfApiModel, tool
from smolagents.agents import ActionStep

# Load environment variables
load_dotenv()

@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
    global driver
    if driver is None:
        return "Browser not initialized"
    
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(f"Match n°{nth_result} not found (only {len(elements)} matches found)")
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result

@tool
def go_back() -> str:
    """Goes back to previous page."""
    global driver
    if driver is None:
        return "Browser not initialized"
    
    driver.back()
    return "Navigated back to previous page"

@tool
def close_popups() -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows!
    This does not work on cookie consent banners.
    """
    global driver
    if driver is None:
        return "Browser not initialized"
    
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    return "Sent escape key to close any popups"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--window-size=1000,1350")
chrome_options.add_argument("--disable-pdf-viewer")
chrome_options.add_argument("--window-position=0,0")

# Initialize the browser - we'll do this lazily to avoid errors on import
driver = None

def initialize_browser():
    """Initialize the Chrome browser with appropriate settings using webdriver-manager"""
    global driver
    if driver is None:
        try:
            # Force webdriver-manager to get latest Chrome driver
            chrome_driver_path = ChromeDriverManager().install()
            
            # Create a Chrome service using the latest driver
            service = Service(chrome_driver_path)
            
            # This will make helium use the chromedriver from webdriver-manager
            os.environ["PATH"] = os.path.dirname(chrome_driver_path) + os.pathsep + os.environ["PATH"]
            
            # Start Chrome browser with helium normally
            driver = helium.start_chrome(headless=False, options=chrome_options)
            return True
        except Exception as e:
            print(f"Error initializing browser: {e}")
            return False
    return True

# Set up screenshot callback
def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    driver = helium.get_driver()
    current_step = memory_step.step_number
    if driver is not None:
        for previous_memory_step in agent.memory.steps:  # Remove previous screenshots for lean processing
            if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
                previous_memory_step.observations_images = None
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"Captured a browser screenshot: {image.size} pixels")
        memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists

    # Update observations with current URL
    url_info = f"Current url: {driver.current_url}"
    memory_step.observations = (
        url_info if memory_step.observations is None else memory_step.observations + "\n" + url_info
    )

# Initialize the model
model_id = "meta-llama/Llama-3.3-70B-Instruct"  # You can change this to your preferred model
model = HfApiModel(model_id=model_id)

# Create the agent
agent = CodeAgent(
    tools=[go_back, close_popups, search_item_ctrl_f],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks=[save_screenshot],
    max_steps=20,
    verbosity_level=2,
)

# Import helium for the agent when needed
def setup_agent():
    """Set up the agent with necessary imports"""
    try:
        agent.python_executor("from helium import *")
        return True
    except TypeError:
        # Different versions of smolagents might have different API
        try:
            agent.python_executor("from helium import *", agent.state)
            return True
        except Exception as e:
            print(f"Error setting up agent: {e}")
            return False

helium_instructions = """
You can use helium to access websites. Don't bother about the helium driver, it's already managed.
We've already ran "from helium import *"
Then you can go to pages!
Code:
go_to('github.com/trending')
```<end_code>

You can directly click clickable elements by inputting the text that appears on them.
Code:
click("Top products")
```<end_code>

If it's a link:
Code:
click(Link("Top products"))
```<end_code>

If you try to interact with an element and it's not found, you'll get a LookupError.
In general stop your action after each button click to see what happens on your screenshot.
Never try to login in a page.

To scroll up or down, use scroll_down or scroll_up with as an argument the number of pixels to scroll from.
Code:
scroll_down(num_pixels=1200) # This will scroll one viewport down
```<end_code>

When you have pop-ups with a cross icon to close, don't try to click the close icon by finding its element or targeting an 'X' element (this most often fails).
Just use your built-in tool `close_popups` to close them:
Code:
close_popups()
```<end_code>

You can use .exists() to check for the existence of an element. For example:
Code:
if Text('Accept cookies?').exists():
    click('I accept')
```<end_code>
"""

def run_wikipedia_search():
    """Example: Search for information on Wikipedia"""
    if not initialize_browser() or not setup_agent():
        return
        
    search_request = """
    Please navigate to https://en.wikipedia.org/wiki/Chicago and give me a sentence containing the word "1992" that mentions a construction accident.
    """
    
    agent_output = agent.run(search_request + helium_instructions)
    print("Final output:")
    print(agent_output)

def run_github_trending_search():
    """Example: Find information about a trending GitHub repo"""
    if not initialize_browser() or not setup_agent():
        return
        
    github_request = """
    I'm trying to find how hard I have to work to get a repo in github.com/trending.
    Can you navigate to the profile for the top author of the top trending repo, and give me their total number of commits over the last year?
    """
    
    agent_output = agent.run(github_request + helium_instructions)
    print("Final output:")
    print(agent_output)

def test_browser():
    """Simple test function to verify web_browser is working correctly"""
    if not initialize_browser() or not setup_agent():
        return False
    
    print("Browser initialized successfully!")
    helium.go_to("https://example.com")
    sleep(2)  # Wait for page to load
    
    # Take a screenshot to verify
    driver = helium.get_driver()
    screenshot_path = "browser_test_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")
    
    # Clean up
    helium.kill_browser()
    return True

if __name__ == "__main__":
    # Uncomment the example you want to run
    # run_wikipedia_search()
    run_github_trending_search()
    # test_browser()

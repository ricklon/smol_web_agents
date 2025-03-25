# -*- coding: utf-8 -*-
"""web_browser module with improved user feedback

Adapted from: https://github.com/huggingface/notebooks/blob/main/smolagents_doc/en/pytorch/web_browser.ipynb
"""

from io import BytesIO
from time import sleep
import os
import logging
import traceback
from typing import Optional, List
import datetime

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

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("web_browser.log")
    ]
)
logger = logging.getLogger(__name__)

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
    
    logger.info(f"Searching for text: '{text}' (match #{nth_result})")
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        msg = f"Match n°{nth_result} not found (only {len(elements)} matches found)"
        logger.warning(msg)
        raise Exception(msg)
    
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", elem)  # Highlight the element
    sleep(0.5)  # Brief pause to make highlighting visible
    result += f" Focused on element {nth_result} of {len(elements)}"
    logger.info(result)
    return result

@tool
def go_back() -> str:
    """Goes back to previous page."""
    global driver
    if driver is None:
        return "Browser not initialized"
    
    logger.info("Navigating back to previous page")
    driver.back()
    sleep(1)  # Give page time to load
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
    
    logger.info("Attempting to close popups with ESC key")
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    return "Sent escape key to close any popups"

@tool
def save_manual_screenshot(filename: Optional[str] = None) -> str:
    """
    Manually saves a screenshot with an optional custom filename.
    Args:
        filename: Optional custom filename (default: timestamp)
    """
    global driver
    if driver is None:
        return "Browser not initialized"
    
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    
    # Ensure the screenshots directory exists
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    filepath = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(filepath)
    logger.info(f"Screenshot saved to {os.path.abspath(filepath)}")
    return f"Screenshot saved to {os.path.abspath(filepath)}"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--window-size=1000,1350")
chrome_options.add_argument("--disable-pdf-viewer")
chrome_options.add_argument("--window-position=0,0")

# Initialize the browser - we'll do this lazily to avoid errors on import
driver = None

def initialize_browser():
    global driver
    if driver is not None:
        logger.info("Browser already initialized")
        return True
    
    try:
        logger.info("Initializing Chrome browser...")

        chrome_driver_path = ChromeDriverManager().install()
        os.environ["PATH"] = (
            os.path.dirname(chrome_driver_path) + os.pathsep + os.environ["PATH"]
        )
        
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--window-size=1000,1350")
        chrome_options.add_argument("--disable-pdf-viewer")
        chrome_options.add_argument("--window-position=0,0")
        # chrome_options.add_argument("--headless")  # uncomment if needed

        driver = helium.start_chrome(headless=False, options=chrome_options)
        logger.info("Browser initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"Error initializing browser: {e}")
        traceback.print_exc()
        return False



# Enhanced screenshot callback with more information
def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    logger.info(f"Taking screenshot for step {memory_step.step_number}")
    sleep(1.5)  # Let JavaScript animations happen before taking the screenshot
    global driver
    
    if driver is None:
        logger.warning("No driver available for screenshot")
        return
        
    current_step = memory_step.step_number
    try:
        # Remove previous screenshots for lean processing
        for previous_memory_step in agent.memory.steps:
            if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
                previous_memory_step.observations_images = None
        
        # Save screenshot
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        logger.info(f"Captured browser screenshot: {image.size} pixels")
        memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists
        
        # Optionally save to disk for debugging
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"step_{current_step}_{timestamp}.png")
        image.save(screenshot_path)
        logger.info(f"Screenshot saved to disk: {screenshot_path}")
        
        # Update observations with current URL and page title
        url_info = f"Current URL: {driver.current_url}"
        title_info = f"Page title: {driver.title}"
        memory_step.observations = (
            "\n".join([url_info, title_info]) 
            if memory_step.observations is None 
            else memory_step.observations + "\n" + "\n".join([url_info, title_info])
        )
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        traceback.print_exc()

# Progress callback to provide real-time feedback
def log_progress(memory_step: ActionStep, agent: CodeAgent) -> None:
    current_step = memory_step.step_number
    logger.info(f"Completed step {current_step}/{agent.max_steps}: {memory_step.action if hasattr(memory_step, 'action') else 'Thinking...'}")
    
    # Print to console as well for immediate feedback
    print(f"Step {current_step}/{agent.max_steps}: {memory_step.action if hasattr(memory_step, 'action') else 'Thinking...'}")

# Initialize the model
def create_agent(model_id: str = "meta-llama/Llama-3.3-70B-Instruct", max_steps: int = 20):
    """Create and configure the agent with specified model"""
    logger.info(f"Initializing agent with model: {model_id}")
    try:
        # Initialize the model
        model = HfApiModel(model_id=model_id)
        
        # Create the agent with enhanced callbacks
        agent = CodeAgent(
            tools=[go_back, close_popups, search_item_ctrl_f, save_manual_screenshot],
            model=model,
            additional_authorized_imports=["helium"],
            step_callbacks=[save_screenshot, log_progress],
            max_steps=max_steps,
            verbosity_level=2,
        )
        
        logger.info("Agent created successfully")
        return agent
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        traceback.print_exc()
        return None

# Import helium for the agent when needed
def setup_agent(agent):
    """Set up the agent with necessary imports"""
    if agent is None:
        logger.error("Cannot setup agent: agent is None")
        return False
        
    try:
        logger.info("Setting up agent with helium imports")
        try:
            agent.python_executor("from helium import *")
            logger.info("Successfully imported helium")
            return True
        except TypeError:
            # Different versions of smolagents might have different API
            agent.python_executor("from helium import *", agent.state)
            logger.info("Successfully imported helium (alternate method)")
            return True
    except Exception as e:
        logger.error(f"Error setting up agent: {e}")
        traceback.print_exc()
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

Save screenshots at important steps using:
Code:
save_manual_screenshot("important_moment.png")
```<end_code>
"""

def run_with_feedback(task_name, request_text, model_id=None, max_steps=20):
    """Run a task with comprehensive feedback throughout the process"""
    print(f"\n{'=' * 50}")
    print(f"Starting task: {task_name}")
    print(f"{'=' * 50}")
    
    # Initialize browser
    if not initialize_browser():
        print("❌ Failed to initialize browser - see logs for details")
        return False
    
    # Create agent
    agent = create_agent(model_id=model_id or "meta-llama/Llama-3.3-70B-Instruct", max_steps=max_steps)
    if agent is None:
        print("❌ Failed to create agent - see logs for details")
        return False
    
    # Setup agent
    if not setup_agent(agent):
        print("❌ Failed to setup agent - see logs for details")
        return False
    
    print(f"\n🔍 Running task: {task_name}")
    print(f"📋 Request: {request_text[:100]}{'...' if len(request_text) > 100 else ''}")
    
    try:
        # Monitor start time
        start_time = datetime.datetime.now()
        print(f"⏱️ Started at: {start_time.strftime('%H:%M:%S')}")
        
        # Run the agent
        agent_output = agent.run(request_text + helium_instructions)
        
        # Calculate duration
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        print(f"\n✅ Task completed in {duration.total_seconds():.2f} seconds")
        print(f"\n📊 Final output:")
        print(f"{'_' * 50}")
        print(agent_output)
        print(f"{'_' * 50}")
        
        # Provide location of screenshots
        screenshots_dir = os.path.abspath("screenshots")
        print(f"\n📸 Screenshots saved to: {screenshots_dir}")
        
        return True
    except Exception as e:
        print(f"\n❌ Error running task: {e}")
        logger.error(f"Error running task '{task_name}': {e}")
        traceback.print_exc()
        return False
    finally:
        # Always provide feedback about where to find logs
        log_file = os.path.abspath("web_browser.log")
        print(f"\n📝 Full logs available at: {log_file}")

def run_wikipedia_search():
    """Search for information on Wikipedia with enhanced feedback"""
    search_request = """
    Please navigate to https://en.wikipedia.org/wiki/Chicago and give me a sentence containing the word "1992" that mentions a construction accident.
    """
    
    return run_with_feedback(
        task_name="Wikipedia Search",
        request_text=search_request,
        max_steps=15
    )

def run_github_trending_search():
    """Find information about a trending GitHub repo with enhanced feedback"""
    github_request = """
    I'm trying to find how hard I have to work to get a repo in github.com/trending.
    Can you navigate to the profile for the top author of the top trending repo, and give me their total number of commits over the last year?
    """
    
    return run_with_feedback(
        task_name="GitHub Trending Search",
        request_text=github_request,
        max_steps=25  # This task might need more steps
    )

def test_browser():
    """Simple test function to verify web_browser is working correctly"""
    print("\n=== Testing Browser Functionality ===")
    
    if not initialize_browser():
        print("❌ Failed to initialize browser")
        return False
    
    print("✅ Browser initialized successfully!")
    
    try:
        print("🌐 Navigating to example.com...")
        helium.go_to("https://example.com")
        sleep(2)  # Wait for page to load
        
        # Take a screenshot to verify
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"browser_test_{timestamp}.png")
        
        driver = helium.get_driver()
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to {os.path.abspath(screenshot_path)}")
        
        print("✅ Test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error during test: {e}")
        logger.error(f"Error during browser test: {e}")
        traceback.print_exc()
        return False
    finally:
        print("🔄 Cleaning up browser instance")
        helium.kill_browser()

def identify_the_forms():
    """Review react web pages and find the form elements on the page."""
    request = """
    Please navigate to http://localhost:5174 and what form options are on the page. 
    There is a Login Form, Signup Form, and an Activity Form. Select each one and take a screen shot. Once those are taken stop.
    """
    
    return run_with_feedback(
        task_name="Find Forms",
        request_text=request,
        max_steps=15
    )

def main():
    """Main function to run tests or tasks based on user input"""
    print("\n=== Web Browser Automation ===")
    print("1. Test Browser")
    print("2. Run Wikipedia Search")
    print("3. Run GitHub Trending Search")
    print("4. Find forms on React page")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        test_browser()
    elif choice == "2":
        run_wikipedia_search()
    elif choice == "3":
        run_github_trending_search()
    elif choice == "4":
        identify_the_forms()
    elif choice == "5":
        print("Exiting...")


    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
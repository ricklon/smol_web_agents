"""Basic web agent using smolagents and helium for web automation."""

import os
from typing import Dict, List, Optional, Any

from colorama import Fore, Style, init
from helium import *
from PIL import Image
from smolagents import CodeAgent, HfApiModel
from smolagents.agents import ActionStep


init(autoreset=True)  # Initialize colorama

class WebAgent(Agent):
    """Web agent that can browse the internet and perform tasks."""
    
    def __init__(self, name: str = "WebAgent"):
        super().__init__(name=name)
        self.browser_open = False
        
    def start_browser(self) -> None:
        """Start the browser if it's not already open."""
        if not self.browser_open:
            start_chrome()
            self.browser_open = True
            print(f"{Fore.GREEN}Browser started.{Style.RESET_ALL}")
            
    def browse_to(self, url: str) -> None:
        """Navigate to a specific URL."""
        self.start_browser()
        go_to(url)
        print(f"{Fore.CYAN}Navigated to: {url}{Style.RESET_ALL}")
        
    def click_element(self, element_identifier: str) -> bool:
        """Click on an element identified by text, CSS selector, or XPath."""
        try:
            click(element_identifier)
            print(f"{Fore.GREEN}Clicked on: {element_identifier}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Failed to click on {element_identifier}: {e}{Style.RESET_ALL}")
            return False
            
    def type_text(self, element_identifier: str, text: str) -> bool:
        """Type text into an input field."""
        try:
            write(text, into=element_identifier)
            print(f"{Fore.GREEN}Typed '{text}' into {element_identifier}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Failed to type into {element_identifier}: {e}{Style.RESET_ALL}")
            return False
            
    def take_screenshot(self, filename: str = "screenshot.png") -> Optional[str]:
        """Take a screenshot of the current page."""
        try:
            screenshot_path = os.path.abspath(filename)
            get_driver().save_screenshot(screenshot_path)
            print(f"{Fore.GREEN}Screenshot saved to: {screenshot_path}{Style.RESET_ALL}")
            return screenshot_path
        except Exception as e:
            print(f"{Fore.RED}Failed to take screenshot: {e}{Style.RESET_ALL}")
            return None
            
    def extract_text(self, element_identifier: str) -> Optional[str]:
        """Extract text from an element."""
        try:
            element = find_all(element_identifier)[0]
            text = element.text
            print(f"{Fore.CYAN}Extracted text: {text[:50]}...{Style.RESET_ALL}" if len(text) > 50 else f"{Fore.CYAN}Extracted text: {text}{Style.RESET_ALL}")
            return text
        except Exception as e:
            print(f"{Fore.RED}Failed to extract text from {element_identifier}: {e}{Style.RESET_ALL}")
            return None
    
    def close_browser(self) -> None:
        """Close the browser."""
        if self.browser_open:
            kill_browser()
            self.browser_open = False
            print(f"{Fore.GREEN}Browser closed.{Style.RESET_ALL}")

def main():
    """Main function to demonstrate the WebAgent."""
    agent = WebAgent()
    
    # Example usage
    agent.browse_to("https://www.google.com")
    agent.type_text("q", "smolagents python")
    agent.click_element("Google Search")
    
    # Allow time to see the results
    import time
    time.sleep(5)
    
    agent.take_screenshot("search_results.png")
    agent.close_browser()

if __name__ == "__main__":
    main()
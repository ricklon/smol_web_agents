import helium
from selenium import webdriver

def initialize_browser():
    print("Initializing Chrome with Helium...")

    # Build a Selenium ChromeOptions object
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--window-size=1000,1350")
    chrome_options.add_argument("--disable-pdf-viewer")
    chrome_options.add_argument("--window-position=0,0")

    # Pass that object to helium.start_chrome()
    driver = helium.start_chrome(
        headless=False,
        options=chrome_options  # Must be a ChromeOptions instance
    )
    print("Browser initialized successfully!")
    return driver

if __name__ == "__main__":
    driver = initialize_browser()
    helium.kill_browser()


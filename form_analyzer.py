"""
Form Analyzer Tool - Identify and extract form fields from web pages.

This tool:
1. Takes a screenshot of a web page
2. Identifies forms and their fields
3. Returns a structured JSON representation of all forms
4. Can be used with Helium automation agents
"""

import os
import json
import logging
import traceback
from time import sleep
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# Third-party imports
import helium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from PIL import Image

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("form_analyzer.log")
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class FormField:
    """Represents a field in a form."""
    name: str
    field_id: str
    field_type: str
    label: str
    required: bool = False
    options: List[str] = field(default_factory=list)
    placeholder: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert field to dictionary."""
        return {
            "name": self.name,
            "id": self.field_id,
            "type": self.field_type,
            "label": self.label,
            "required": self.required,
            "options": self.options,
            "placeholder": self.placeholder
        }

@dataclass
class Form:
    """Represents a form with its fields."""
    name: str
    form_id: str
    fields: List[FormField] = field(default_factory=list)
    submit_button: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert form to dictionary."""
        return {
            "name": self.name,
            "id": self.form_id,
            "fields": [field.to_dict() for field in self.fields],
            "submit_button": self.submit_button
        }

class FormAnalyzer:
    """Analyzes forms on a web page and extracts structured information."""
    
    def __init__(self, headless: bool = False):
        """Initialize the FormAnalyzer.
        
        Args:
            headless: Whether to run the browser in headless mode
        """
        self.driver = None
        self.headless = headless
        self.screenshots_dir = "form_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    def initialize_browser(self) -> bool:
        """Initialize the browser."""
        try:
            logger.info("Initializing browser...")
            
            # Setup Chrome options
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--window-size=1920,1080")
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Initialize browser using helium (which uses selenium under the hood)
            self.driver = helium.start_chrome(headless=self.headless, options=chrome_options)
            
            logger.info("Browser initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing browser: {e}")
            traceback.print_exc()
            return False
    
    def navigate_to(self, url: str) -> bool:
        """Navigate to the specified URL.
        
        Args:
            url: The URL to navigate to
            
        Returns:
            bool: True if navigation was successful, False otherwise
        """
        if self.driver is None:
            if not self.initialize_browser():
                return False
        
        try:
            logger.info(f"Navigating to {url}")
            helium.go_to(url)
            # Wait for page to load
            sleep(2)
            return True
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            traceback.print_exc()
            return False
    
    def take_screenshot(self, name: str = "page") -> Optional[str]:
        """Take a screenshot of the current page.
        
        Args:
            name: Base name for the screenshot file
            
        Returns:
            Optional[str]: Path to the screenshot or None if failed
        """
        if self.driver is None:
            logger.error("Browser not initialized")
            return None
            
        try:
            file_path = os.path.join(self.screenshots_dir, f"{name}.png")
            self.driver.save_screenshot(file_path)
            logger.info(f"Screenshot saved to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            traceback.print_exc()
            return None
    
    def identify_forms(self) -> List[Form]:
        """Identify all forms on the page based on the test-forms.tsx structure.
        
        This function specifically looks for the forms in the provided React component
        where forms are shown/hidden based on state.
        
        Returns:
            List[Form]: List of forms identified on the page
        """
        if self.driver is None:
            logger.error("Browser not initialized")
            return []
        
        forms = []
        
        try:
            # Wait for page content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            
            # Find the form selector buttons to identify available forms
            form_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'px-4 py-2 rounded')]")
            form_types = [btn.text for btn in form_buttons]
            
            logger.info(f"Found form types: {form_types}")
            
            # Process each form by clicking its button
            for i, form_type in enumerate(form_types):
                form_name = form_type.strip()
                
                # Click the form button to display it
                logger.info(f"Clicking on {form_name} button")
                form_buttons[i].click()
                sleep(1)  # Give time for the form to appear
                
                # Take a screenshot of this form
                self.take_screenshot(f"{form_name.lower().replace(' ', '_')}_form")
                
                # Find the form container
                form_container = self.driver.find_element(By.XPATH, "//div[contains(@class, 'bg-white p-6 rounded shadow-md')]")
                
                # Extract form ID (using a placeholder since the React components don't have explicit IDs)
                form_id = form_name.lower().replace(" ", "_")
                
                # Create a Form object
                current_form = Form(name=form_name, form_id=form_id)
                
                # Find form fields in the current form
                self._extract_form_fields(form_container, current_form)
                
                # Find submit button
                submit_buttons = form_container.find_elements(By.XPATH, ".//button[@type='submit']")
                if submit_buttons:
                    current_form.submit_button = submit_buttons[0].text
                
                forms.append(current_form)
            
            return forms
            
        except Exception as e:
            logger.error(f"Error identifying forms: {e}")
            traceback.print_exc()
            return []
    
    def _extract_form_fields(self, form_element: webdriver.remote.webelement.WebElement, form: Form) -> None:
        """Extract all fields from the form element.
        
        Args:
            form_element: The form WebElement to extract fields from
            form: The Form object to populate with fields
        """
        try:
            # Find all input elements in the form
            inputs = form_element.find_elements(By.XPATH, ".//input")
            textareas = form_element.find_elements(By.XPATH, ".//textarea")
            selects = form_element.find_elements(By.XPATH, ".//select")
            
            # Process standard inputs
            for input_elem in inputs:
                self._process_input_field(input_elem, form)
            
            # Process textareas
            for textarea in textareas:
                field_id = textarea.get_attribute("id") or ""
                name = textarea.get_attribute("name") or ""
                placeholder = textarea.get_attribute("placeholder") or ""
                required = textarea.get_attribute("required") is not None
                
                # Try to find associated label
                label_text = self._find_label_text(form_element, field_id)
                
                field = FormField(
                    name=name,
                    field_id=field_id,
                    field_type="textarea",
                    label=label_text,
                    required=required,
                    placeholder=placeholder
                )
                form.fields.append(field)
            
            # Process select dropdowns
            for select in selects:
                field_id = select.get_attribute("id") or ""
                name = select.get_attribute("name") or ""
                required = select.get_attribute("required") is not None
                
                # Try to find associated label
                label_text = self._find_label_text(form_element, field_id)
                
                # Get options
                options = []
                option_elements = select.find_elements(By.XPATH, ".//option")
                for option in option_elements:
                    option_text = option.text
                    if option_text:
                        options.append(option_text)
                
                field = FormField(
                    name=name,
                    field_id=field_id,
                    field_type="select",
                    label=label_text,
                    required=required,
                    options=options
                )
                form.fields.append(field)
                
        except Exception as e:
            logger.error(f"Error extracting form fields: {e}")
            traceback.print_exc()
    
    def _process_input_field(self, input_elem: webdriver.remote.webelement.WebElement, form: Form) -> None:
        """Process an input field and add it to the form.
        
        Args:
            input_elem: The input WebElement to process
            form: The Form object to add the field to
        """
        try:
            field_type = input_elem.get_attribute("type") or "text"
            field_id = input_elem.get_attribute("id") or ""
            name = input_elem.get_attribute("name") or ""
            placeholder = input_elem.get_attribute("placeholder") or ""
            required = input_elem.get_attribute("required") is not None
            
            # Skip hidden inputs
            if field_type == "hidden":
                return
                
            # Try to find associated label
            label_text = self._find_label_text(form.fields[0].label if form.fields else "", field_id)
            
            # For checkbox/radio inputs within groups, they often share the same name
            # but have different values
            value = input_elem.get_attribute("value") or ""
            
            # Special handling for checkboxes and radio buttons
            if field_type in ["checkbox", "radio"]:
                # For these types, we want to find the text next to them
                # This is typically in a <span> next to the input inside a label
                parent_label = input_elem.find_element(By.XPATH, "./..") if input_elem.tag_name != "label" else input_elem
                
                if parent_label.tag_name == "label":
                    # Get text excluding the input element's text
                    label_spans = parent_label.find_elements(By.XPATH, ".//span")
                    if label_spans:
                        label_text = label_spans[0].text
                    else:
                        # If no span, try to get the label text directly
                        label_text = parent_label.text
                
                # For checkboxes/radios with the same name (like in a group), 
                # check if we already have this field group
                existing_field = next((f for f in form.fields if f.name == name and f.field_type == field_type), None)
                
                if existing_field:
                    # Add this option to the existing field
                    existing_field.options.append(value or label_text)
                    return
            
            field = FormField(
                name=name,
                field_id=field_id,
                field_type=field_type,
                label=label_text,
                required=required,
                placeholder=placeholder
            )
            
            # Add options for checkbox/radio
            if field_type in ["checkbox", "radio"]:
                field.options.append(value or label_text)
                
            form.fields.append(field)
                
        except Exception as e:
            logger.error(f"Error processing input field: {e}")
            traceback.print_exc()
    
    def _find_label_text(self, parent_element: Any, field_id: str) -> str:
        """Find the label text for a field.
        
        Args:
            parent_element: The parent element containing the label
            field_id: The ID of the field to find the label for
            
        Returns:
            str: The label text or empty string if not found
        """
        if not field_id:
            return ""
            
        try:
            # Try to find a label with a 'for' attribute matching the field ID
            if isinstance(parent_element, webdriver.remote.webelement.WebElement):
                labels = parent_element.find_elements(By.XPATH, f".//label[@for='{field_id}']")
                if labels:
                    return labels[0].text.strip()
            
            # If no matching 'for' attribute, return empty string
            return ""
        except Exception:
            return ""
    
    def analyze_page(self, url: str) -> Dict[str, Any]:
        """Analyze a web page and extract all forms and their fields.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dict[str, Any]: JSON-serializable dictionary with form information
        """
        result = {
            "success": False,
            "url": url,
            "forms": [],
            "screenshots": [],
            "error": None
        }
        
        try:
            # Navigate to the page
            if not self.navigate_to(url):
                result["error"] = "Failed to navigate to the URL"
                return result
            
            # Take a screenshot of the full page
            full_screenshot = self.take_screenshot("full_page")
            if full_screenshot:
                result["screenshots"].append(full_screenshot)
            
            # Identify forms
            forms = self.identify_forms()
            
            # Convert forms to dictionaries
            result["forms"] = [form.to_dict() for form in forms]
            result["success"] = True
            
            return result
        except Exception as e:
            logger.error(f"Error analyzing page: {e}")
            traceback.print_exc()
            result["error"] = str(e)
            return result
        finally:
            # Clean up
            if self.driver:
                logger.info("Closing browser")
                helium.kill_browser()
                self.driver = None
    
    def generate_helium_script(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a Helium script to fill and submit the forms.
        
        Args:
            analysis_result: The result from analyze_page()
            
        Returns:
            str: Python code for interacting with the forms using Helium
        """
        if not analysis_result["success"] or not analysis_result["forms"]:
            return "# No valid forms found to generate script for"
        
        lines = [
            "# Auto-generated Helium script for form interaction",
            "from helium import *",
            "from time import sleep",
            "",
            f"# Navigate to the target page",
            f"go_to('{analysis_result['url']}')",
            "sleep(2)  # Wait for page to load",
            ""
        ]
        
        # For each form, create a function to fill it
        for form in analysis_result["forms"]:
            form_name = form["name"].lower().replace(" ", "_")
            lines.append(f"def fill_{form_name}_form():")
            lines.append(f"    # Click the {form['name']} button to show the form")
            lines.append(f"    click('{form['name']}')")
            lines.append("    sleep(1)  # Wait for form to appear")
            lines.append("")
            
            # Fill each field
            lines.append("    # Fill form fields")
            for field in form["fields"]:
                if field["type"] == "text" or field["type"] == "email" or field["type"] == "password" or field["type"] == "tel" or field["type"] == "date":
                    lines.append(f"    write('example_{field['name']}', into='{field['label']}')")
                elif field["type"] == "textarea":
                    lines.append(f"    write('Sample text for {field['name']}', into='{field['label']}')")
                elif field["type"] == "select":
                    if field["options"] and len(field["options"]) > 1:
                        # Select the second option (index 1) to avoid the placeholder
                        option = field["options"][1]
                        lines.append(f"    select('{option}', from_='{field['label']}')")
                elif field["type"] == "checkbox":
                    lines.append(f"    click('{field['label']}')")
                elif field["type"] == "radio":
                    if field["options"]:
                        option = field["options"][0]
                        lines.append(f"    click('{option}')")
            
            # Submit the form
            if form["submit_button"]:
                lines.append("")
                lines.append("    # Submit the form")
                lines.append(f"    click('{form['submit_button']}')")
                lines.append("    sleep(1)  # Wait for submission")
                lines.append("    # Handle any confirmation dialogs here if needed")
            
            lines.append("")
        
        # Add a main section to call each form function
        lines.append("# Main execution")
        lines.append("if __name__ == '__main__':")
        for form in analysis_result["forms"]:
            form_name = form["name"].lower().replace(" ", "_")
            lines.append(f"    fill_{form_name}_form()")
            lines.append("    # You can add verification code here to check if form submission was successful")
            lines.append("")
        
        lines.append("    # Close the browser when done")
        lines.append("    kill_browser()")
        
        return "\n".join(lines)
    
    def to_json(self, analysis_result: Dict[str, Any], indent: int = 2) -> str:
        """Convert analysis result to a pretty-printed JSON string.
        
        Args:
            analysis_result: The result from analyze_page()
            indent: Indentation level for JSON formatting
            
        Returns:
            str: Pretty-printed JSON
        """
        return json.dumps(analysis_result, indent=indent)
    
    def save_result(self, analysis_result: Dict[str, Any], output_file: str = "form_analysis.json") -> bool:
        """Save the analysis result to a JSON file.
        
        Args:
            analysis_result: The result from analyze_page()
            output_file: The file path to save the result to
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(analysis_result, f, indent=2)
            logger.info(f"Analysis result saved to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving analysis result: {e}")
            traceback.print_exc()
            return False


# Example usage
def main():
    """Run the form analyzer on a sample page."""
    analyzer = FormAnalyzer(headless=False)
    
    # Analyze the page
    result = analyzer.analyze_page("http://localhost:5174")
    
    # Save the result
    analyzer.save_result(result)
    
    # Generate Helium script
    script = analyzer.generate_helium_script(result)
    
    # Save the script
    with open("form_interaction_script.py", "w") as f:
        f.write(script)
    
    # Print summary
    print(f"\nAnalysis complete. Found {len(result['forms'])} forms.")
    for form in result['forms']:
        print(f"- {form['name']}: {len(form['fields'])} fields")
    
    print(f"\nFull analysis saved to: form_analysis.json")
    print(f"Helium script saved to: form_interaction_script.py")
    print(f"Screenshots saved to: {analyzer.screenshots_dir}")

if __name__ == "__main__":
    main()

# Form Analyzer Tool

A powerful tool for automated form analysis, testing, and verification. This tool can scan web pages, identify forms and their fields, and generate structured JSON data that can be used by automation agents.

## Features

- **Automatic Form Detection**: Identifies all forms on a web page
- **Field Analysis**: Extracts detailed information about form fields including:
  - Field types (text, checkbox, select, etc.)
  - Labels
  - Required status
  - Options for select/checkbox/radio fields
- **Screenshot Capture**: Takes screenshots of each form for visual verification
- **JSON Output**: Provides structured data for automation tools
- **Helium Script Generation**: Automatically creates scripts for filling forms
- **AI Agent Integration**: Works with SmolaGents for intelligent form testing

## Installation

### Prerequisites

- Python 3.8+
- Chrome or Chromium browser installed

### Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements include:
- selenium
- helium
- Pillow (PIL)
- smolagents (for AI integration)

## Basic Usage

### Analyze Forms on a Page

```python
from form_analyzer import FormAnalyzer

# Initialize analyzer
analyzer = FormAnalyzer(headless=False)  # Set headless=True for no UI

# Analyze a page
result = analyzer.analyze_page("http://localhost:5174")

# Save results to JSON
analyzer.save_result(result, "form_analysis.json")

# Generate Helium script for automation
script = analyzer.generate_helium_script(result)
with open("form_interaction_script.py", "w") as f:
    f.write(script)
```

### Run the Demo

For a quick demonstration:

```bash
python demo_script.py
```

This will:
1. Open the test forms page
2. Analyze all forms
3. Generate JSON output and a Helium script
4. Display analysis results

## Integration with AI Agents

The tool is designed to work with SmolaGents for AI-powered form testing:

```python
from form_analyzer_usage import run_form_test

# Define test instructions
instructions = """
Please test the login form with:
- Email: test@example.com
- Password: password123
- Remember me: checked
"""

# Run AI-powered test
run_form_test("http://localhost:5174", instructions)
```

## JSON Output Format

The tool generates JSON data with this structure:

```json
{
  "success": true,
  "url": "http://localhost:5174",
  "forms": [
    {
      "name": "Login Form",
      "id": "login_form",
      "fields": [
        {
          "name": "email",
          "id": "email",
          "type": "email",
          "label": "Email Address",
          "required": true,
          "options": [],
          "placeholder": ""
        },
        // Additional fields...
      ],
      "submit_button": "Log In"
    },
    // Additional forms...
  ],
  "screenshots": [
    "/path/to/screenshot1.png",
    // Additional screenshots...
  ],
  "error": null
}
```

## Examples

### Testing Login Form

```python
from form_analyzer_usage import test_login_form

# Run predefined login form test
test_login_form()
```

### Testing All Forms

```python
from form_analyzer_usage import test_login_form, test_signup_form, test_activity_form

# Run all tests
test_login_form()
test_signup_form()
test_activity_form()
```

## Project Structure

- `form_analyzer.py` - Core form analysis functionality
- `form_analyzer_usage.py` - Integration with SmolaGents
- `demo_script.py` - Demonstration script
- `form_screenshots/` - Screenshots of analyzed forms
- `form_analyzer_output/` - Generated JSON and automation scripts
- `agent_screenshots/` - Screenshots from AI agent testing

## Customization

You can customize the analyzer behavior:

```python
analyzer = FormAnalyzer(
    headless=True  # Run without visible browser
)

# Customize screenshot directory
analyzer.screenshots_dir = "custom_screenshots"

# Analyze with custom handling
result = analyzer.analyze_page("https://example.com/forms")
```

## Troubleshooting

- **Browser Issues**: Make sure Chrome/Chromium is installed and up-to-date
- **Form Detection Issues**: Check if forms use non-standard HTML structures
- **Field Extraction Errors**: For complex forms, you may need to modify the field extraction logic

## License

MIT License

## Credits

Created for use with [SmolaGents](https://github.com/huggingface/smolagents) web automation framework.

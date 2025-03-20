"""
Form Analyzer Demo Script

This script demonstrates how to:
1. Analyze forms on a webpage
2. Generate structured JSON output
3. Generate a Helium automation script
"""

from form_analyzer import FormAnalyzer
import json
import os
from pprint import pprint

def run_demo():
    """Run a demonstration of the form analyzer."""
    print("\n" + "=" * 60)
    print("Form Analyzer Demonstration".center(60))
    print("=" * 60)
    
    # URL with test forms
    url = "http://localhost:5174"
    
    print(f"\n🔍 Analyzing forms at: {url}")
    print("This will open a browser window and analyze all forms on the page...")
    
    # Initialize the analyzer
    analyzer = FormAnalyzer(headless=False)
    
    # Analyze the page
    result = analyzer.analyze_page(url)
    
    if not result["success"]:
        print(f"\n❌ Analysis failed: {result['error']}")
        return
    
    # Print summary of findings
    print("\n✅ Analysis complete!")
    print(f"\nFound {len(result['forms'])} forms:")
    
    for i, form in enumerate(result["forms"], 1):
        print(f"\n{i}. {form['name']}:")
        print(f"   - Fields: {len(form['fields'])}")
        print(f"   - Submit Button: {form['submit_button']}")
        
        # Print first few fields as example
        print("   - Field Examples:")
        for j, field in enumerate(form['fields'][:3], 1):
            print(f"     {j}. {field['label']} ({field['type']})")
        
        if len(form['fields']) > 3:
            print(f"     ... and {len(form['fields']) - 3} more fields")
    
    # Save results
    output_dir = "form_analyzer_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save JSON result
    json_path = os.path.join(output_dir, "form_analysis.json")
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)
    
    # Generate Helium script
    script = analyzer.generate_helium_script(result)
    script_path = os.path.join(output_dir, "form_interaction.py")
    with open(script_path, "w") as f:
        f.write(script)
    
    print("\n" + "=" * 60)
    print("Output Files Generated".center(60))
    print("=" * 60)
    print(f"\n📊 JSON Analysis: {os.path.abspath(json_path)}")
    print(f"🤖 Helium Script: {os.path.abspath(script_path)}")
    print(f"📸 Screenshots: {os.path.abspath(analyzer.screenshots_dir)}")
    
    # Display JSON example
    print("\n" + "=" * 60)
    print("JSON Output Example (First Form)".center(60))
    print("=" * 60)
    
    if result["forms"]:
        first_form = result["forms"][0]
        # Convert to JSON string with indentation for display
        form_json = json.dumps(first_form, indent=2)
        # Print just a preview (first 20 lines) if it's long
        form_json_lines = form_json.split("\n")
        if len(form_json_lines) > 20:
            print("\n".join(form_json_lines[:20]))
            print("... [truncated for brevity] ...")
        else:
            print(form_json)
    
    print("\n" + "=" * 60)
    print("Demo Complete".center(60))
    print("=" * 60)

if __name__ == "__main__":
    run_demo()

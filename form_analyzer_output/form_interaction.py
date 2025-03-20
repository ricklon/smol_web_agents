# Auto-generated Helium script for form interaction
from helium import *
from time import sleep

# Navigate to the target page
go_to('http://localhost:5174')
sleep(2)  # Wait for page to load

def fill_login_form_form():
    # Click the Login Form button to show the form
    click('Login Form')
    sleep(1)  # Wait for form to appear

    # Fill form fields
    write('example_email', into='')
    write('example_password', into='')
    click('Remember me')

    # Submit the form
    click('Log In')
    sleep(1)  # Wait for submission
    # Handle any confirmation dialogs here if needed

def fill_signup_form_form():
    # Click the Signup Form button to show the form
    click('Signup Form')
    sleep(1)  # Wait for form to appear

    # Fill form fields
    write('example_firstName', into='')
    write('example_lastName', into='')
    write('example_email', into='')
    write('example_phone', into='')
    write('example_password', into='')
    write('example_confirmPassword', into='')
    write('example_birthDate', into='')
    write('example_occupation', into='')
    click('Technology')
    click('I accept the Terms and Conditions')
    select('Male', from_='Gender')
    select('United States', from_='Country')

    # Submit the form
    click('Create Account')
    sleep(1)  # Wait for submission
    # Handle any confirmation dialogs here if needed

def fill_activity_form_form():
    # Click the Activity Form button to show the form
    click('Activity Form')
    sleep(1)  # Wait for form to appear

    # Fill form fields
    write('example_activityName', into='')
    write('example_location', into='')
    write('example_date', into='')
    write('example_participants', into='')
    click('low')
    click('This activity requires equipment')
    click('Email')
    write('Sample text for description', into='Description')
    select('Meeting', from_='Activity Type')
    select('Daily', from_='Recurrence')

    # Submit the form
    click('Schedule Activity')
    sleep(1)  # Wait for submission
    # Handle any confirmation dialogs here if needed

# Main execution
if __name__ == '__main__':
    fill_login_form_form()
    # You can add verification code here to check if form submission was successful

    fill_signup_form_form()
    # You can add verification code here to check if form submission was successful

    fill_activity_form_form()
    # You can add verification code here to check if form submission was successful

    # Close the browser when done
    kill_browser()
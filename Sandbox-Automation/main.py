from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from flask import Flask, request, jsonify

"""

MAIN BUGS
1. Account credentials, need to be made
2. Linking to Clan Life
3. Calibration for removal based on Slack website, biggest issue

"""

app = Flask(__name__)

# Slack login credentials
SLACK_EMAIL = "YOUR_EMAIL" # Fill once account details are made
SLACK_PASSWORD = "YOUR_PASSWORD" # Fill once account details are made
SLACK_WORKSPACE_URL = "https://app.slack.com/client/T282LTWJC/C282HVA84"

def remove_user(email):
    # Setup Chrome WebDriver
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\chromedriver.exe')  # Change the path
    driver.get(SLACK_WORKSPACE_URL)

    # Log in to Slack
    driver.find_element(By.ID, "email").send_keys(SLACK_EMAIL)
    driver.find_element(By.ID, "password").send_keys(SLACK_PASSWORD)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    # Allow some time to load
    time.sleep(5)

    # Search for the user
    driver.get(f"{SLACK_WORKSPACE_URL}/admin")

    # Assume there is a search functionality to find members by email (this part needs Slack admin access)
    search_box = driver.find_element(By.ID, 'search-input')  # This is an example, adapt it to Slack's interface
    search_box.send_keys(email)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

    # Find the user and remove them (depends on how Slack displays this option in the UI)
    remove_button = driver.find_element(By.CLASS_NAME, 'remove-user')  # Replace with the actual button class or ID
    remove_button.click()

    time.sleep(2)
    driver.quit()

@app.route('/remove_users', methods=['POST'])
def remove_users():
    data = request.get_json()
    emails = data['emails']

    for email in emails:
        remove_user(email)

    return jsonify({'status': 'success', 'message': 'Users removed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

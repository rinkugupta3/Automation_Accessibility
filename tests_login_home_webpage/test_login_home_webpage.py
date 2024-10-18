# WCAG 2.1 AXE-CORE V 4.10.0 for Automation testing https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js
# pytest -v tests_login_home_webpage/test_login_home_webpage.py
import os
import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from axe_selenium_python import Axe
from selenium.webdriver.support.ui import WebDriverWait

from modules.html_report_generator import generate_html_report

# Get logger from pytest setup
logger = logging.getLogger(__name__)


def test_accessibility():
    # Set up the Selenium WebDriver (Chrome) using Service object
    logger.info("Setting up Chrome WebDriver")
    options = Options()
    # options.add_argument("--headless")  # Optional: Run Chrome in headless mode (no UI)
    service = Service(ChromeDriverManager().install())  # Use Service to manage the ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the webpage
        logger.info("Navigating to login page")
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        # Wait for the login form element to ensure the page has fully loaded
        logger.info("Waiting for the login form to be present on the page")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))

        # Input the username
        logger.info("Entering username")
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("Admin")

        # Input the password
        logger.info("Entering password")
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin123")

        # Click the login button
        logger.info("Clicking login button")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Wait for the dashboard page to load
        logger.info("Waiting for the dashboard page to load")
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))

        # Inject the latest axe-core script (version 4.10.0 from CDN)
        logger.info("Injecting axe-core JavaScript into the page")
        driver.execute_script("""
            var script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js';
            document.head.appendChild(script);
        """)

        # Wait for the script to fully load before proceeding
        logger.info("Waiting for axe-core script to load")
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return typeof axe !== 'undefined'"))

        # Initialize Axe for accessibility testing
        logger.info("Initializing Axe-core for accessibility testing")
        axe = Axe(driver)

        # Run the WCAG 2.1 audit
        logger.info("Running WCAG 2.1 accessibility audit")
        results = axe.run()

        # Output the results to a JSON file
        logger.info("Writing results to accessibility_report.json")
        axe.write_results(results, 'tests_login_home_webpage/accessibility_report.json')

        # Output the results to a HTML file by calling the imported function html_report_path
        logger.info("Generating accessibility HTML report")
        # html_report_path = os.path.join('tests_login_webpage/accessibility_report.html')
        html_report_path = 'tests_login_home_webpage/accessibility_report.html'
        generate_html_report(results, html_report_path)

        # Extract all result types
        violations = results.get("violations", [])
        passes = results.get("passes", [])
        inapplicable = results.get("inapplicable", [])
        incomplete = results.get("incomplete", [])

        # Log violations in pytest.log
        if len(violations) == 0:
            logger.info("No accessibility violations found!")
        else:
            logger.info(f"{len(violations)} accessibility violations found:")
            for violation in violations:
                logger.info(f"Violation: {violation['description']}")
                logger.info(f"Impact: {violation['impact']}")
                for node in violation["nodes"]:
                    logger.info(f"Element: {node['html']}")
                    logger.info(f"Failure Summary: {node['failureSummary']}")

        # Log passed tests_login_axecore_lighthouse.py
        if len(passes) > 0:
            logger.info(f"{len(passes)} accessibility tests passed:")
            for passed in passes:
                logger.info(f"Passed: {passed['description']}")

        # Log inapplicable tests_login_axecore_lighthouse.py
        if len(inapplicable) > 0:
            logger.info(f"{len(inapplicable)} tests were inapplicable:")
            for item in inapplicable:
                logger.info(f"Inapplicable: {item['description']}")

        # Log incomplete tests_login_axecore_lighthouse.py
        if len(incomplete) > 0:
            logger.info(f"{len(incomplete)} tests were incomplete:")
            for item in incomplete:
                logger.info(f"Incomplete: {item['description']}")

    finally:
        # Close the browser
        logger.info("Closing the browser")
        driver.quit()

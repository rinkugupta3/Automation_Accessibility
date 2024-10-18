# WCAG 2.1 AXE-CORE V 4.10.0 for Automation testing https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js
# pytest -v tests_login_webpage/test_login_webpage.py
import logging
import os
import time
from selenium import webdriver
from axe_selenium_python import Axe
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
        # driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        driver.get("https://rinkugupta3.github.io/HTML_CSS_Portfolio/")

        # Wait for the login form element to ensure the page has fully loaded
        logger.info("Waiting for the login form to be present on the page")
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        time.sleep(30)

        # Inject the latest axe-core script (version 4.10.0 from CDN)
        logger.info("Injecting axe-core JavaScript into the page")
        driver.execute_script("""
            var script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js';
            document.head.appendChild(script);
        """)

        # Wait for the script to fully load before proceeding
        logger.info("Waiting for axe-core script to load")
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return typeof axe !== 'undefined'"))

        # Initialize Axe for accessibility testing
        logger.info("Initializing Axe-core for accessibility testing")
        axe = Axe(driver)

        # Run the WCAG 2.1 audit
        logger.info("Running WCAG 2.1 accessibility audit")
        results = axe.run()

        # Log violations in pytest.log
        violations = results["violations"]

        if len(violations) == 0:
            logger.info("No accessibility violations found!")
        else:
            logger.info(f"{len(violations)} accessibility violations found:")
            for violation in violations:
                logger.info(f"Violation: {violation['description']}")
                logger.info(f"Impact: {violation['impact']}")
                logger.info(f"Learn more: {violation['helpUrl']}")

                for node in violation["nodes"]:
                    logger.info(f"Element: {node['html']}")
                    logger.info(f"Failure Summary: {node['failureSummary']}")

        # Output the results to a JSON file
        logger.info("Generating accessibility JSON report")
        axe.write_results(results, 'tests_login_webpage/accessibility_report.json')

        # Generate and output the HTML report by calling the imported function
        logger.info("Generating accessibility HTML report")
        # html_report_path = os.path.join('tests_login_webpage/accessibility_report.html')
        html_report_path = 'tests_login_webpage/accessibility_report.html'
        generate_html_report(results, html_report_path)

    finally:
        # Close the browser
        logger.info("Closing the browser")
        driver.quit()


"""
    # Check for violations and log the results
    violations = results["violations"]
    if len(violations) == 0:
        logger.info("No accessibility violations found!")
        print("No accessibility violations found!")
    else:
        logger.info(f"{len(violations)} accessibility violations found")
        print(f"{len(violations)} accessibility violations found:")
        for violation in violations:
            logger.info(f"Violation: {violation['description']}")
            logger.info(f"Impact: {violation['impact']}")
            for node in violation["nodes"]:
                logger.info(f"Element: {node['html']}")
                logger.info(f"Failure Summary: {node['failureSummary']}")
                print(f"\nViolation: {violation['description']}")
                print(f"Impact: {violation['impact']}")
                print(f"Element: {node['html']}")
                print(f"Failure Summary: {node['failureSummary']}")
    
    # Generate and output the HTML report for better readability
    logger.info("Generating accessibility HTML report")
    axe.write_results(results, 'tests_login_webpage/accessibility_report.html')

    # Check for violations and log the results
    logger.info("Checking accessibility violations...")
    violations = results["violations"]
    if len(violations) == 0:
        logger.info("No accessibility violations found!")
    else:
        logger.info(f"{len(violations)} accessibility violations found")
        for violation in violations:
            if violation["nodes"]:
                logger.info(f"Violation: {violation['description']}")
                logger.info(f"Impact: {violation['impact']}")
                for node in violation["nodes"]:
                    logger.info(f"Element: {node['html']}")
                    logger.info(f"Failure Summary: {node['failureSummary']}")
            else:
                logger.info(f"Inapplicable rule: {violation['description']}")
                
                
    # Generate and output the HTML report for better readability
    logger.info("Generating accessibility HTML report")
    html_report_path = os.path.join('tests_login_webpage/accessibility_report.html')
    with open(html_report_path, 'w') as html_file:
        html_file.write("<html><head><title>Accessibility Report</title></head><body>")
        html_file.write("<h1>Accessibility Report</h1>")
        if results['violations']:
            html_file.write("<h2>Violations</h2><ul>")
            for violation in results["violations"]:
                html_file.write(f"<li><strong>{violation['description']}</strong><br>")
                html_file.write(f"Impact: {violation['impact']}<br>")
                html_file.write(f"<a href='{violation['helpUrl']}'>Learn more</a><br>")
                html_file.write("<ul>")
                for node in violation['nodes']:
                    html_file.write(f"<li>Element: {node['html']}</li>")
                    html_file.write(f"<li>Failure Summary: {node['failureSummary']}</li>")
                html_file.write("</ul></li>")
            html_file.write("</ul>")
        else:
            html_file.write("<h2>No accessibility violations found!</h2>")
        html_file.write("</body></html>")

    logger.info("Accessibility HTML report generated successfully.")
"""

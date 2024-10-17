# npm install -g lighthouse
# lighthouse_command = [r"C:\Users\<YourUsername>\AppData\Roaming\npm\lighthouse.cmd", "https://your-url.com"]
# Axe-core for accessibility checks
# Lighthouse for performance checks
# Axe-core provides detailed reports about accessibility violations, including the specific elements affected and suggestions for remediation.
# Lighthouse gives a high-level overview of accessibility issues alongside other performance and SEO metrics
# pytest -vv tests_axecore_lighthouse/test_axecore_lighthouse.py
import logging
import os
import platform
import subprocess
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

# Set up the Selenium WebDriver (Chrome) using Service object
logger.info("Setting up Chrome WebDriver")
options = Options()
options.add_argument("--headless")  # Optional: Run Chrome in headless mode (no UI)
service = Service(ChromeDriverManager().install())  # Use Service to manage the ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    logger.info("Navigating to login page")
    # driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # driver.get("https://rinkugupta3.github.io/HTML_CSS_Portfolio/")
    driver.get("https://www.google.com/")

    # Wait for the login form element to ensure the page has fully loaded
    logger.info("Waiting for the login form to be present on the page")
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "APjFqb")))
    # time.sleep(30)

    """
    # Input apple.com in search box
    search_box = driver.find_element(By.ID, "APjFqb")
    search_box.send_keys('apple.com')
    # click enter button
    driver.get(
        'https://www.google.com/search?q=apple.com&sca_esv=b11b22a906989fea&source=hp&ei=k4ARZ9B9koKb1w_c3Z6xBA'
        '&iflsig=AL9hbdgAAAAAZxGOo-vmlxu7yW9QGVFUpWznZEZ3_om5&ved=0ahUKEwiQk42BrZaJAxUSweYEHdyuJ0YQ4dUDCA8&uact=5&oq'
        '=apple.com&gs_lp'
        '=Egdnd3Mtd2l6IglhcHBsZS5jb20yCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyBRAAGIAEMggQABiABBixAzIIEAAYgAQYsQMyCxAAGIAEGLEDGIMBMggQABiABBixAzIFEAAYgAQyBRAAGIAESKeLAlCDyQFY-9sBcAJ4AJABAJgBN6ABygOqAQE5uAEDyAEA-AEBmAILoALzA6gCCsICEBAAGAMY5QIY6gIYjAMYjwHCAhAQLhgDGOUCGOoCGIwDGI8BwgIREC4YgAQYsQMY0QMYgwEYxwHCAg4QLhiABBixAxjRAxjHAcICCxAuGIAEGNEDGMcBwgILEC4YgAQYsQMYgwHCAgsQLhiABBixAxjlBMICCBAAGIAEGMkDwgILEAAYgAQYkgMYigXCAggQABiABBiSA8ICBRAuGIAEmAMGkgcCMTGgB5di&sclient=gws-wiz')
    """

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
    axe.write_results(results, 'tests_axecore_lighthouse/accessibility_report.json')

    # Generate and output the HTML report by calling the imported function
    logger.info("Generating accessibility HTML report")
    html_report_path = 'tests_axecore_lighthouse/accessibility_report.html'
    generate_html_report(results, html_report_path)

    # Path to Lighthouse executable
    # lighthouse_path = r"C:\Users\dhira\AppData\Roaming\npm\lighthouse.cmd"
    lighthouse_command = "lighthouse"
    subprocess.run([lighthouse_command])

    # Run Lighthouse audit
    logger.info("Running Lighthouse audit...")

    # Define the output path for the Lighthouse report
    # output_path = 'tests_axecore_lighthouse/lighthouse_report.json'
    output_path = 'tests_axecore_lighthouse/lighthouse_report.html'
    generate_html_report(results, html_report_path)

    lighthouse_command = [
        "lighthouse",
        # "https://rinkugupta3.github.io/HTML_CSS_Portfolio/",
        # "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
        "https://www.google.com/",
        "--output=html",
        f"--output-path={output_path}",  # Set the output path for the Lighthouse report
        "--quite"
    ]
    subprocess.run(lighthouse_command)

    logger.info("Lighthouse audit complete. Results saved to lighthouse_report.html.")

finally:
    # Close the browser
    logger.info("Closing the browser")
    driver.quit()

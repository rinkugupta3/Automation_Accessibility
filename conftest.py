# Dynamically Set log_file per Test via pytest Hooks: Use pytest hooks to dynamically configure the log file per test
# suite or directory. The pytest hooks allow setting up logging for each test or suite dynamically without
# interfering with pytest's logging setup.
import os
import pytest
import logging


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Get the current test file being executed
    test_name = config.getoption("file_or_dir")[0] if config.getoption("file_or_dir") else "pytest"

    # Define log directory and ensure it exists
    log_dir_map = {
        'test_axecore_lighthouse.py': 'tests',
        'test_login_home_webpage.py': 'tests_login_home_webpage',
        'test_login_webpage.py': 'tests_login_webpage',
    }

    log_dir = log_dir_map.get(os.path.basename(test_name), 'logs')  # Default 'logs' folder for unknown tests

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set log file path dynamically
    log_file_path = os.path.join(log_dir, 'pytest.log')

    # Update log file configuration in pytest
    config.option.log_file = log_file_path

    # Configure logging
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    logging.info(f"Logging setup complete. Logs will be saved to: {log_file_path}")

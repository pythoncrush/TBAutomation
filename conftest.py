from datetime import datetime
import pytest
import logging


def pytest_configure(config):
	if not config.option.log_file:
		timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")
		config.option.log_file = "pytest_debug_log_" + timestamp + ".log"
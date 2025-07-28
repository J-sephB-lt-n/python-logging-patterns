"""
Global setup of loggers for this application
"""

import atexit
import json
import logging.config
from pathlib import Path


def setup_logging():
    """
    Perform once-off global logger setup
    """
    config_file: Path = Path("utils/logging/config.json")
    with open(config_file, "r") as file:
        log_config = json.load(file)

    logging.config.dictConfig(log_config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

"""
Entry point of the application
"""

import logging

from utils.logging import setup_logging

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("app")
    logger.info("Started application", extra={"note": "some extra info here"})
    logger.warning("An example warning message")

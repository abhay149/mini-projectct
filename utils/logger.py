import logging
import os

LOG_DIR = "logs"
LOG_FILE = "aris.log"

# Create logs folder if not exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_path = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ARIS")


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)


def log_debug(message):
    logger.debug(message)
<<<<<<< HEAD
import logging
import os
from logging.handlers import RotatingFileHandler

# Create a logs directory if it doesn't exist
LOG_DIR = "logs"
try:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
except Exception as e:
    print(f"Error creating log directory: {e}")

# Define log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Environment-based log levels (DEBUG for development, WARNING for production)
log_level = logging.DEBUG if os.getenv('ENV') == 'development' else logging.WARNING

# Logging configuration
logging.basicConfig(
    level=log_level,  # Dynamically set log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3),  # Rotating file handler (5MB per file, keep 3 backups)
        logging.StreamHandler()  # Log to the console
    ]
)

# Initialize the logger
logger = logging.getLogger("app_logger")

logger.info("Logging system initialized.")
=======
import logging
import os
from logging.handlers import RotatingFileHandler

# Create a logs directory if it doesn't exist
LOG_DIR = "logs"
try:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
except Exception as e:
    print(f"Error creating log directory: {e}")

# Define log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Environment-based log levels (DEBUG for development, WARNING for production)
log_level = logging.DEBUG if os.getenv('ENV') == 'development' else logging.WARNING

# Logging configuration
logging.basicConfig(
    level=log_level,  # Dynamically set log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3),  # Rotating file handler (5MB per file, keep 3 backups)
        logging.StreamHandler()  # Log to the console
    ]
)

# Initialize the logger
logger = logging.getLogger("app_logger")

logger.info("Logging system initialized.")
>>>>>>> dc8cfbe92444c4d49f3be126b10a798f1295dd81

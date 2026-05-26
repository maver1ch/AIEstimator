import logging
import sys
from backend.core.config import settings

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL.upper())
    
    # Avoid duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

setup_logging()

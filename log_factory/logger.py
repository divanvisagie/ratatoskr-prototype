import logging

log_filename = "logs/app.log"

# Configure the file handler
file_handler = logging.FileHandler(log_filename)
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
file_handler.setFormatter(logging.Formatter(log_format))

def create_logger(name: str) -> logging.Logger:
    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger

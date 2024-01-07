import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


def configure_logger():
    """
    Configures a logger with a specific level and stream handler.

    Returns:
        logging.Logger: The configured logger object.

    Example:
        To use this logger in your application, you can call this function as follows:

            from utils import logger_config

            # Configure logger with custom level
            logger = logger_config.configure_logger()
            logger.error("An example error message.")
    """

    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    logger = logging.getLogger(__name__)

    return logger

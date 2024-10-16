import colorama
from colorama import init
import logging
import sys
from typing import Optional


# Initialize colorama
init(autoreset=True)  # Automatically reset colors after each print

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter to add color to logging levels.
    """

    # ANSI Color Codes
    COLORS = {
        'DEBUG': '\033[0;95m',   # Purple
        'INFO': '\033[0;36m',    # Cyan
        'WARNING': '\033[0;33m', # Yellow
        'ERROR': '\033[0;31m',   # Red
        'CRITICAL': '\033[1;31m',# Bold Red
        'SUCCESS': '\033[0;32m', # Green
    }

    def format(self, record: logging.LogRecord) -> str:
        level_name = record.levelname

        # Apply color to the level name if it matches a defined color
        if level_name in self.COLORS:
            level_name_color = f"{self.COLORS[level_name]}{level_name}\033[0m"  # Reset after level name
            record.levelname = level_name_color

        return super().format(record)

def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.DEBUG,
                 timestamp_format: str = '%Y-%m-%d %H:%M:%S') -> logging.Logger:
    """
    Set up a logger with specified name, level, and optional file output.

    Args:
        name (str): Name of the logger.
        log_file (Optional[str]): Optional log file name for file output.
        level (int): Logging level.
        timestamp_format (str): Format for timestamps in log messages.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logging.addLevelName(25, "SUCCESS")  # Add custom log level

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = ColoredFormatter(
        f'{colorama.Fore.LIGHTBLACK_EX}%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt=timestamp_format
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)

            # Use a simple formatter for file output
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt=timestamp_format
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to create file handler for logging: {e}")

    return logger

# Setup the logger for the bot
_logger = setup_logger("BOT", log_file="bot.log")

def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.

    Returns:
        logging.Logger: The logger instance.
    """
    return _logger

if __name__ == "__main__":
    # Example logging messages
    _logger.debug("This is a debug message")
    _logger.info("This is an info message")
    _logger.warning("This is a warning message")
    _logger.error("This is an error message")
    _logger.critical("This is a critical message")
    _logger.log(25, "This is a success message")

import os
import json
import logging
from typing import Any, Dict, Tuple
from disnake.ext import commands
from jsonschema import validate, ValidationError


class CogManager:
    """
    Manages the loading and unloading of cogs for a Discord bot.
    """

    def __init__(self, bot: commands.InteractionBot | Any, *, path: str = "cogs"):
        """
        Initializes the CogManager with the bot instance and path for cogs.

        Args:
            bot (commands.InteractionBot | Any): The bot instance.
            path (str): The directory path where cogs are located.
        """
        self.bot = bot
        self.path = os.path.join(os.getcwd(), path)

        # Set up the logger
        self.logger = self._setup_logger()

        self.cogs: list[str] = []
        self.errors: Dict[str, Exception] = {}

    def _setup_logger(self) -> logging.Logger:
        """
        Sets up the logger for the CogManager.

        Returns:
            logging.Logger: The logger instance.
        """
        if "BOT" in logging.Logger.manager.loggerDict:
            return logging.getLogger("BOT")
        else:
            logger = logging.getLogger(__name__)
            logger.warning("No logger named 'BOT' found. Using the default logger.")
            return logger

    def load_cogs(self) -> Tuple[list[str], Dict[str, Exception]]:
        """
        Loads all cogs from the specified path.

        Returns:
            Tuple[list[str], Dict[str, Exception]]: A tuple containing the list of loaded cogs and any loading errors.
        """
        for file in os.listdir(self.path):
            if file.endswith(".py"):
                try:
                    self.bot.load_extension(f"{self.path.replace('/', '.')[:-1]}.{file[:-3]}")
                    self.cogs.append(file)
                except Exception as e:
                    self.errors[f"cogs.{file[:-3]}"] = e
                    self.logger.error(f"Failed to load cog {file}: {e}")
        return self.cogs, self.errors


class ConfigManager:
    """
    Manages the loading and validation of the bot's configuration.
    """

    CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "TOKEN": {"type": "string"},
        },
        "required": ["TOKEN"],
    }

    def __init__(self, bot: commands.InteractionBot | Any, *, path: str = "data"):
        """
        Initializes the ConfigManager with the bot instance and path for configuration.

        Args:
            bot (commands.InteractionBot | Any): The bot instance.
            path (str): The directory path where configuration files are located.
        """
        self.bot = bot
        self.path = os.path.join(os.getcwd(), path)
        self.config_file = os.path.join(self.path, "config.json")

        # Set up the logger
        self.logger = self._setup_logger()

        self.config: Dict[str, Any] = {}

        # Load the configuration
        self.load_configs()

    def _setup_logger(self) -> logging.Logger:
        """
        Sets up the logger for the ConfigManager.

        Returns:
            logging.Logger: The logger instance.
        """
        if "BOT" in logging.Logger.manager.loggerDict:
            return logging.getLogger("BOT")
        else:
            logger = logging.getLogger(__name__)
            logger.warning("No logger named 'BOT' found. Using the default logger.")
            return logger

    def load_configs(self) -> None:
        """
        Loads the configuration from a JSON file.
        """
        try:
            if not os.path.exists(self.config_file):
                self.logger.error(f"Config file '{self.config_file}' not found.")
                return

            with open(self.config_file, "r") as f:
                config_data = json.load(f)

            # Validate the configuration against the schema
            validate(instance=config_data, schema=self.CONFIG_SCHEMA)
            self.config = config_data
            self.logger.info("Configuration loaded successfully.")

        except FileNotFoundError:
            self.logger.error(f"Config file '{self.config_file}' not found.")
        except json.JSONDecodeError:
            self.logger.error("Error decoding JSON from the config file.")
        except ValidationError as ve:
            self.logger.error(f"Configuration validation error: {ve.message}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while loading config: {e}")

    def get_token(self) -> Optional[str]:
        """
        Returns the bot token from the configuration.

        Returns:
            Optional[str]: The bot token, or None if not found.
        """
        return self.config.get("TOKEN")

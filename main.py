from disnake import ApplicationCommandInteraction
from disnake.ext.commands import errors
from utils.logger import get_logger
from utils.utils import CogManager
from disnake.ext import commands
import disnake

logger = get_logger()


class ErrorEmbed:
    """
    A utility class for creating error embeds.
    """

    @staticmethod
    def create_error_embed(error: str, additional_info: str = None) -> disnake.Embed:
        """
        Creates a formatted error embed.

        Args:
            error (str): The main error message.
            additional_info (str, optional): Additional context about the error.

        Returns:
            disnake.Embed: The error embed.
        """
        embed = disnake.Embed(
            title="__An error occurred__",
            description="**Error:**\n" + error + "\n\n" +
                        ("**Additional info:**\n" + additional_info if additional_info else ""),
            color=disnake.Color.red()
        )
        return embed


class Bot(commands.InteractionBot):
    """
    Custom bot class that extends disnake's InteractionBot with additional functionality.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Bot instance and its cog manager.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.cog_manager = CogManager(self)

    async def on_ready(self) -> None:
        """Called when the bot connects to Discord's API."""
        logger.info(f"Logged in as {self.user}")
        cogs, loading_errors = self.cog_manager.load_cogs()
        logger.info(f"Loaded cogs: {cogs}")
        if loading_errors:
            logger.error(f"Failed to load cogs: {loading_errors}")

    async def on_slash_command_error(
            self, interaction: ApplicationCommandInteraction, error: errors.CommandError
    ) -> None:
        """
        Handles errors that occur during command execution.

        Args:
            interaction (ApplicationCommandInteraction): The interaction that triggered the command.
            error (errors.CommandError): The error that occurred.
        """
        logger.error(f"Error occurred in command '{interaction.data.get('name')}': {error}")

        # Create an error embed based on the specific error type
        embed = self._get_error_embed(error)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def _get_error_embed(self, error: errors.CommandError) -> disnake.Embed:
        """
        Generates an error embed based on the error type.

        Args:
            error (errors.CommandError): The error that occurred.

        Returns:
            disnake.Embed: The generated error embed.
        """
        error_map = {
            errors.ExpectedClosingQuoteError: (
                "Expected closing quote",
                f"Closing quote: {error.close_quote}"
            ),
            errors.ConversionError: (
                "Conversion error",
                f"Failed to convert argument: {error.converter}\nOriginal Exception: {error.original}"
            ),
            errors.MissingRequiredArgument: (
                "Missing required argument",
                f"The argument `{error.param.name}` is required but was not provided."
            ),
            errors.TooManyArguments: (
                "Too many arguments",
                "You have provided too many arguments for this command."
            ),
            errors.BadArgument: (
                "Bad argument",
                "One or more arguments provided are invalid."
            ),
            errors.CheckFailure: (
                "Check failure",
                "You do not have permission to run this command."
            ),
            errors.CommandNotFound: (
                "Command not found",
                "The command you tried to invoke does not exist."
            ),
            errors.DisabledCommand: (
                "Disabled command",
                "This command is currently disabled."
            ),
            errors.CommandInvokeError: (
                "Command invocation error",
                f"The command raised an error: {error.original}"
            ),
            errors.CommandOnCooldown: (
                "Command on cooldown",
                f"You need to wait `{error.retry_after:.2f}` seconds before using this command again."
            ),
            errors.MaxConcurrencyReached: (
                "Max concurrency reached",
                f"This command is currently being used by too many users ({error.number}). Please try again later."
            ),
            errors.UserInputError: (
                "User input error",
                "There was a problem with your input. Please check your command and try again."
            ),
            errors.ObjectNotFound: (
                "Object not found",
                f"The specified object could not be found. Object: `{error.argument}`"
            ),
            errors.MemberNotFound: (
                "Member not found",
                f"The specified member `{error.argument}` could not be found."
            ),
            errors.GuildNotFound: (
                "Guild not found",
                f"The specified guild `{error.argument}` could not be found."
            ),
            errors.UserNotFound: (
                "User not found",
                f"The specified user `{error.argument}` could not be found."
            ),
            errors.ChannelNotFound: (
                "Channel not found",
                f"The specified channel `{error.argument}` could not be found."
            ),
            errors.ThreadNotFound: (
                "Thread not found",
                f"The specified thread `{error.argument}` could not be found."
            ),
            errors.ChannelNotReadable: (
                "Channel not readable",
                f"The bot cannot read messages in `{error.argument.mention}` (`{error.argument.id}`)."
            ),
            errors.BadColourArgument: (
                "Invalid color argument",
                f"The specified color `{error.argument}` is not valid."
            ),
            errors.RoleNotFound: (
                "Role not found",
                f"The specified role `{error.argument}` could not be found."
            ),
            errors.BadInviteArgument: (
                "Invalid invite",
                f"The specified invite link `{error.argument}` is invalid or expired."
            ),
            errors.EmojiNotFound: (
                "Emoji not found",
                f"The specified emoji `{error.argument}` could not be found."
            ),
            errors.GuildStickerNotFound: (
                "Sticker not found",
                f"The specified sticker `{error.argument}` could not be found."
            ),
            errors.GuildScheduledEventNotFound: (
                "Scheduled event not found",
                f"The specified scheduled event `{error.argument}` could not be found."
            ),
            errors.PartialEmojiConversionFailure: (
                "Partial emoji conversion failure",
                f"The specified emoji `{error.argument}` could not be converted."
            ),
            errors.BadBoolArgument: (
                "Bad boolean argument",
                f"The specified boolean argument `{error.argument}` is not recognized."
            ),
            errors.LargeIntConversionFailure: (
                "Large integer conversion failure",
                f"The specified argument `{error.argument}` could not be converted to an integer."
            ),
            errors.DisabledCommand: (
                "Disabled command",
                "This command is currently disabled."
            ),
            errors.MissingRole: (
                "Missing role",
                f"You are missing `{error.missing_role!r}` to run this command."
            ),
            errors.BotMissingRole: (
                "Bot missing role",
                f"The bot is missing `{error.missing_role!r}` to run this command."
            ),
            errors.MissingAnyRole: (
                "Missing any role",
                f"You are missing at least one of these roles to run this command: {', '.join(error.missing_roles)}"
            ),
            errors.BotMissingAnyRole: (
                "Bot missing any role",
                f"The bot is missing at least one of these roles to run this command: {', '.join(error.missing_roles)}"
            ),
            errors.MissingPermissions: (
                "Missing permissions",
                f"You are missing {', '.join([f'`{perm.replace("_", " ").replace("guild", "server").title()}`' for perm in error.missing_permissions])} permission(s) to run this command."
            ),
            errors.BotMissingPermissions: (
                "Bot missing permissions",
                f"The bot is missing {', '.join([f'`{perm.replace("_", " ").replace("guild", "server").title()}`' for perm in error.missing_permissions])} permission(s) to run this command."
            ),
            errors.NSFWChannelRequired: (
                "NSFW channel required",
                "This command can only be used in NSFW channels."
            ),
            errors.BadUnionArgument: (
                "Bad union argument",
                "The argument could not be converted to any of the expected types."
            ),
            errors.BadLiteralArgument: (
                "Bad literal argument",
                "The argument did not match any of the expected literal values."
            ),
            errors.ArgumentParsingError: (
                "Argument parsing error",
                "There was an issue while parsing your input."
            ),
            errors.UnexpectedQuoteError: (
                "Unexpected quote error",
                f"Unexpected quote mark: {error.quote!r} found in input."
            ),
            errors.InvalidEndOfQuotedStringError: (
                "Invalid end of quoted string",
                f"Expected space after closing quote but received: {error.char!r}."
            ),
            errors.ExtensionError: (
                "Extension error",
                f"An error occurred with an extension: {error.name}."
            ),
            errors.ExtensionAlreadyLoaded: (
                "Extension already loaded",
                f"The extension `{error.name}` is already loaded."
            ),
            errors.ExtensionNotLoaded: (
                "Extension not loaded",
                f"The extension `{error.name}` has not been loaded."
            ),
            errors.NoEntryPointError: (
                "No entry point error",
                f"The extension `{error.name}` has no 'setup' function."
            ),
            errors.ExtensionFailed: (
                "Extension failed",
                f"The extension `{error.name}` failed to load: {error.original}"
            ),
            errors.ExtensionNotFound: (
                "Extension not found",
                f"The extension `{error.name}` could not be found."
            ),
            errors.CommandRegistrationError: (
                "Command registration error",
                f"The command `{error.name}` is already an existing command or alias."
            ),
            errors.FlagError: (
                "Flag error",
                "There was an issue with parsing flags."
            ),
            errors.TooManyFlags: (
                "Too many flags",
                f"Flag `{error.flag.name}` received too many values. Expected {error.flag.max_args} but received {len(error.values)}."
            ),
            errors.BadFlagArgument: (
                "Bad flag argument",
                f"Could not convert to `{error.flag.annotation.__name__}` for flag `{error.flag.name}`."
            ),
            errors.MissingRequiredFlag: (
                "Missing required flag",
                f"Flag `{error.flag.name}` is required and missing."
            ),
            errors.MissingFlagArgument: (
                "Missing flag argument",
                f"Flag `{error.flag.name}` does not have an argument."
            ),
            errors.PrivateMessageOnly: (
                "Private message only",
                "This command can only be used in a private message."
            ),
            errors.NoPrivateMessage: (
                "No private message",
                "This command cannot be used in a private message."
            ),
            errors.NotOwner: (
                "Not owner",
                "You are not the owner of this bot."
            ),
            errors.CheckAnyFailure: (
                "Check Failed",
                "You do not have permission to run this command."
            ),
            errors.MessageNotFound: (
                "Message not found",
                f"The specified message `{error.argument}` could not be found."
            ),
            errors.BadColorArgument: (
                "Bad color argument",
                f"The specified color `{error.argument}` is not valid."
            )
        }

        # Default error handling if no specific error handling is defined
        default_error = ("Unknown error", "An unexpected error occurred. Please try again later.")

        # Get the embed based on the error type, or use the default if not found
        return ErrorEmbed.create_error_embed(
            *error_map.get(type(error), default_error)
        )


# Instantiate the bot with all intents enabled
bot = Bot(intents=disnake.Intents.all())

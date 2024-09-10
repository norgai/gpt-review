"""The GPT CLI configuration and utilities."""
import os
import sys
from collections import OrderedDict

from knack import CLI, CLICommandsLoader

from gpt_review import __version__
from gpt_review._ask import AskCommandGroup
from gpt_review._git import GitCommandGroup
from gpt_review._review import ReviewCommandGroup
from gpt_review.repositories.github import GitHubCommandGroup

CLI_NAME = "gpt"


class GPTCLI(CLI):
    """Custom CLI implemntation to set version for the GPT CLI."""

    def get_cli_version(self) -> str:
        return __version__


class GPTCommandsLoader(CLICommandsLoader):
    """The GPT CLI Commands Loader."""

    _CommandGroups = [AskCommandGroup, GitHubCommandGroup, GitCommandGroup, ReviewCommandGroup]

    def load_command_table(self, args) -> OrderedDict:
        for command_group in self._CommandGroups:
            command_group.load_command_table(self)
        return OrderedDict(self.command_table)

    def load_arguments(self, command) -> None:
        for argument_group in self._CommandGroups:
            argument_group.load_arguments(self)
        super(GPTCommandsLoader, self).load_arguments(command)


def cli() -> int:

    setuo_logging()

    """The GPT CLI entry point."""
    gpt = GPTCLI(
        cli_name=CLI_NAME,
        config_dir=os.path.expanduser(os.path.join("~", f".{CLI_NAME}")),
        config_env_var_prefix=CLI_NAME,
        commands_loader_cls=GPTCommandsLoader,
    )
    return gpt.invoke(sys.argv[1:])

def setuo_logging():
    """Setup logging for the CLI."""
    import logging

    # Configure the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG for detailed output

    # Create a stream handler to log to stdout (captured by GitHub Actions)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Set the format for the logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

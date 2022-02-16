import sys
from pathlib import Path

from loguru import logger


def add_logging_sink(sink, verbose: int, colorize=False, serialize=False):
    message_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "- <level>{message}</level>"
    )
    if verbose == 0:

        def quiet_filter(record):
            return record.get("extra", {}).get("queue", None) == "all"

        logger.add(
            sink,
            colorize=colorize,
            level="INFO",
            format=message_format,
            filter=quiet_filter,
            serialize=serialize,
        )
    elif verbose == 1:
        logger.add(
            sink, colorize=colorize, level="INFO", format=message_format, serialize=serialize
        )
    elif verbose >= 2:
        logger.add(
            sink, colorize=colorize, level="DEBUG", format=message_format, serialize=serialize
        )


def configure_master_process_logging_to_terminal(
    verbose: int, process_name: str = "psimulate"
):
    if process_name != "psimulate":
        # We don't have individual queue logs to silence
        # which is what verbosity 0 does.
        verbose += 1
    logger.remove()  # Clear default configuration
    add_logging_sink(sys.stdout, verbose, colorize=True)


def configure_master_process_logging_to_file(output_directory: Path):
    master_log = output_directory / "master.log"
    serial_log = output_directory / "master.log.json"
    add_logging_sink(master_log, verbose=2)
    add_logging_sink(serial_log, verbose=2, serialize=True)

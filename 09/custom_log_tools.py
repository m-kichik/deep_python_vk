import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):
    LOG_COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[90m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[31m",
    }

    def format(self, record):
        log_time = datetime.now()
        log_level_color = self.LOG_COLORS.get(record.levelname, "\033[0m")

        log_message = super().format(record)

        formatted_message = (
            f"{log_time}\t"
            + f"{log_level_color}{record.levelname}\033[0m\t{record.name}\t{log_message}"
        )

        return formatted_message


class CustomFilter(logging.Filter):
    def filter(self, record):
        log_message = record.msg
        return len(log_message.split()) >= 5

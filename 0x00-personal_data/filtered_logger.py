#!/usr/bin/env python3
"""
This module function returns the log message obfuscated
"""

from typing import List
import logging
from logging import StreamHandler
import re
import csv


rgx = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object named "user_data".

    Returns:
        logging.Logger: Logger object for logging user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """
    Obfuscate specified fields in a log message.

    Arguments:
    fields: list of strings representing fields to obfuscate
    redaction: string representing the replacement for obfuscated fields
    message: string representing the log line
    separator: string representing the character separating fields
    in the log line

    Returns:
            String: Log message with specified fields obfuscated.
    """
    extract, replace = (rgx["extract"], rgx["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        Initialize RedactingFormatter with a list of fields to redact.

        Args:
            fields (list): List of strings representing fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, filtering values for specified fields.
        Args:
            record (logging.LogRecord): The log record to format.
        Returns:
            str: Formatted log message.
        """
        message = record.getMessage()
        for field in self.fields:
            message = filter_datum(
                [field], self.REDACTION, message, self.SEPARATOR)
        record.msg = message
        return super().format(record)

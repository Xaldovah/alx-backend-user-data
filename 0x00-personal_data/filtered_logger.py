#!/usr/bin/env python3
"""
This module function returns the log message obfuscated
"""

import os
from typing import List
import logging
from logging import StreamHandler
import re
import csv
import mysql.connector


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


def get_db():
    """
    Returns a connector to the database.

    Returns:
    mysql.connector.connection.MySQLConnection: Connector to the database.
    """
    # Get database credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the database
    try:
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        print("Connected to the database successfully!")
        return connection
    except mysql.connector.Error as err:
        print("Error:", err)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecords
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt

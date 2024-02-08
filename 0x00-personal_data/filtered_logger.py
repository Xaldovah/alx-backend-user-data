#!/usr/bin/env python3
"""
This module function returns the log message obfuscated
"""

from typing import List
import re

rgx = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
data = ("name", "email", "phone", "ssn", "password")


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

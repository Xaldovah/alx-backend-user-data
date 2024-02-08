#!/usr/bin/env python3
"""
This module function returns the log message obfuscated
"""

import re


def filter_datum(fields, redaction, message, separator):
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
    pattern = re.compile(r'({}=)([^;]+)'.format('|'.join(fields), re.escape(
        separator)))
    return pattern.sub(r'\1' + redaction, message)

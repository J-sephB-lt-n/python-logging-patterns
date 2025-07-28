"""
Global logger setup for structured logging in JSON format.

This module provides custom logging components that enable structured logging
in JSON format, making logs easier to parse and analyze with tools like
ELK Stack, Splunk, or other log aggregation systems.

Key components:
- JsonFormatter: Formats log records as JSON strings
"""

import datetime as dt
import json
import logging
from typing import override

# Set of built-in attributes in the LogRecord class
# Used to identify custom attributes added to log records
LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "taskName",
    "thread",
    "threadName",
}


class JsonFormatter(logging.Formatter):
    """
    Custom log formatter that outputs log records as JSON strings.

    This formatter converts Python logging.LogRecord objects into JSON format,
    which is useful for structured logging and easier log parsing by log
    management systems.

    Features:
    - Formats log records as JSON objects
    - Includes standard fields like message and timestamp
    - Preserves exception and stack trace information
    - Allows custom field mapping through fmt_keys
    - Automatically includes any custom attributes added to LogRecord

    Args:
        fmt_keys: Optional dictionary mapping output field names to LogRecord attribute names.
                 For example, {'log_level': 'levelname'} would include the level name
                 in the output JSON with the key 'log_level'.
    """

    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
        indent: bool | None = None,
    ):
        """
        Initialize the JSON formatter.

        Args:
            fmt_keys: Dictionary mapping output field names to LogRecord attribute names.
        """
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}
        self.indent = indent

    @override
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON string.
        """
        message = self._prepare_log_dict(record)
        return json.dumps(
            message,
            default=str,
            indent=self.indent,
        )

    def _prepare_log_dict(self, record: logging.LogRecord):
        """
        Prepare a dictionary representation of the log record.

        This method builds a dictionary containing all relevant information from
        the log record, including standard fields, custom fields specified in fmt_keys,
        and any additional custom attributes attached to the record.
        """
        # Always include these fields in the output
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),  # ISO 8601 timestamp with UTC timezone
        }

        # Add exception info if present
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        # Add stack trace info if present
        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        # Apply custom field mapping from fmt_keys
        # This creates a dictionary with keys from fmt_keys and values from either:
        # 1. The corresponding value in always_fields (if it exists)
        # 2. The attribute from the record with the name specified in fmt_keys
        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }

        # Add any remaining always_fields that weren't mapped through fmt_keys
        message.update(always_fields)

        # Add any custom attributes that were added to the LogRecord
        # (attributes not in the standard LogRecord attributes list)
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    """
    Filter that only allows log records with levels less than or equal to INFO.

    This filter is useful for separating non-error logs (DEBUG, INFO) from
    error logs (WARNING, ERROR, CRITICAL).
    """

    @override
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= logging.INFO

"""Custom exception types and error-detail formatting utilities."""

import sys
import traceback
from types import ModuleType


class CustomException(Exception):
    """Exception that includes the source location of the original error."""

    def __init__(self, error_message: Exception, error_detail: ModuleType = sys):
        """Initialize a custom exception with source details.

        Args:
            error_message: The original exception.
            error_detail: Module exposing ``exc_info()``. Defaults to ``sys``.
        """
        self.error_message = self.error_message_detail(error_message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def error_message_detail(error: Exception, error_detail: ModuleType = sys) -> str:
        """Format an exception with its originating file and line number.

        Args:
            error: The original exception.
            error_detail: Module exposing ``exc_info()``. Defaults to ``sys``.

        Returns:
            A human-readable error message with source location details.
        """
        _, _, exc_tb = error_detail.exc_info()
        if exc_tb is None:
            exc_tb = error.__traceback__

        if exc_tb is None:
            return f"Error occurred in python script: {error!s}"

        frame = traceback.extract_tb(exc_tb)[-1]
        return (
            "Error occurred in python script:\n"
            f"\t~ name: {frame.filename}\n"
            f"\t~ line number: {frame.lineno}\n"
            f"\t~ error message: {error!s}"
        )

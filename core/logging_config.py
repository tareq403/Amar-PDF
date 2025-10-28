"""
Logging configuration for PDF Editor application
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class PDFEditorLogger:
    """
    Centralized logging configuration for the PDF Editor application.

    Provides both file and console logging with configurable levels.
    Logs are stored in a 'logs' directory with timestamped filenames.
    """

    _instance: Optional['PDFEditorLogger'] = None
    _initialized: bool = False

    def __new__(cls):
        """Singleton pattern to ensure only one logger instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the logger (only once)"""
        if PDFEditorLogger._initialized:
            return

        self.logger = logging.getLogger('PDFEditor')
        self.logger.setLevel(logging.DEBUG)  # Capture all levels

        # Prevent duplicate handlers
        if self.logger.handlers:
            return

        # Create logs directory if it doesn't exist
        self.log_dir = Path(__file__).parent.parent / 'logs'
        self.log_dir.mkdir(exist_ok=True)

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        # File handler - detailed logging
        log_filename = f"pdf_editor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(self.log_dir / log_filename, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)

        # Console handler - only warnings and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        PDFEditorLogger._initialized = True
        self.logger.info("=== PDF Editor Logger Initialized ===")

    def get_logger(self) -> logging.Logger:
        """
        Get the logger instance.

        Returns:
            Configured logger instance
        """
        return self.logger

    def set_console_level(self, level: int) -> None:
        """
        Set the console logging level.

        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO)
        """
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(level)
                self.logger.info(f"Console logging level set to {logging.getLevelName(level)}")

    def set_file_level(self, level: int) -> None:
        """
        Set the file logging level.

        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO)
        """
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setLevel(level)
                self.logger.info(f"File logging level set to {logging.getLevelName(level)}")


def get_logger() -> logging.Logger:
    """
    Convenience function to get the PDF Editor logger.

    Returns:
        Configured logger instance

    Example:
        >>> from core.logging_config import get_logger
        >>> logger = get_logger()
        >>> logger.info("PDF file opened successfully")
        >>> logger.error("Failed to save PDF", exc_info=True)
    """
    return PDFEditorLogger().get_logger()


def log_function_call(func):
    """
    Decorator to log function calls with arguments and return values.

    Args:
        func: Function to decorate

    Example:
        >>> @log_function_call
        >>> def open_pdf(filepath):
        >>>     return True
    """
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        func_name = func.__name__

        # Log function call
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"Calling {func_name}({signature})")

        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func_name} returned {result!r}")
            return result
        except Exception as e:
            logger.error(f"{func_name} raised {type(e).__name__}: {e}", exc_info=True)
            raise

    return wrapper


def log_performance(func):
    """
    Decorator to log function execution time.

    Args:
        func: Function to decorate

    Example:
        >>> @log_performance
        >>> def render_page(page_num):
        >>>     # rendering code
        >>>     pass
    """
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        func_name = func.__name__

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.debug(f"{func_name} completed in {elapsed_time:.4f} seconds")
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"{func_name} failed after {elapsed_time:.4f} seconds", exc_info=True)
            raise

    return wrapper

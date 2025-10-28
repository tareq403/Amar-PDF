"""
Custom exceptions for PDF Editor application
"""


class PDFEditorException(Exception):
    """
    Base exception for all PDF Editor errors.

    All custom exceptions in the application inherit from this class,
    making it easy to catch any application-specific error.
    """
    pass


# PDF-related exceptions

class PDFException(PDFEditorException):
    """Base exception for PDF-related errors"""
    pass


class PDFOpenError(PDFException):
    """Raised when a PDF file cannot be opened"""
    def __init__(self, filepath: str, reason: str = ""):
        self.filepath = filepath
        self.reason = reason
        message = f"Failed to open PDF file: {filepath}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class PDFSaveError(PDFException):
    """Raised when a PDF file cannot be saved"""
    def __init__(self, filepath: str, reason: str = ""):
        self.filepath = filepath
        self.reason = reason
        message = f"Failed to save PDF file: {filepath}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class PDFRenderError(PDFException):
    """Raised when a PDF page cannot be rendered"""
    def __init__(self, page_num: int, reason: str = ""):
        self.page_num = page_num
        self.reason = reason
        message = f"Failed to render PDF page {page_num}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class PDFMergeError(PDFException):
    """Raised when PDF files cannot be merged"""
    def __init__(self, source_file: str, reason: str = ""):
        self.source_file = source_file
        self.reason = reason
        message = f"Failed to merge PDF: {source_file}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class InvalidPageNumberError(PDFException):
    """Raised when an invalid page number is provided"""
    def __init__(self, page_num: int, total_pages: int):
        self.page_num = page_num
        self.total_pages = total_pages
        message = f"Invalid page number {page_num}. Document has {total_pages} pages (0-indexed)."
        super().__init__(message)


# Annotation-related exceptions

class AnnotationException(PDFEditorException):
    """Base exception for annotation-related errors"""
    pass


class InvalidAnnotationDataError(AnnotationException):
    """Raised when annotation data is invalid"""
    def __init__(self, annotation_type: str, reason: str):
        self.annotation_type = annotation_type
        self.reason = reason
        message = f"Invalid {annotation_type} annotation data: {reason}"
        super().__init__(message)


class AnnotationRenderError(AnnotationException):
    """Raised when an annotation cannot be rendered"""
    def __init__(self, annotation_type: str, reason: str = ""):
        self.annotation_type = annotation_type
        self.reason = reason
        message = f"Failed to render {annotation_type} annotation"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


# File-related exceptions

class FileException(PDFEditorException):
    """Base exception for file operation errors"""
    pass


class ImageLoadError(FileException):
    """Raised when an image file cannot be loaded"""
    def __init__(self, filepath: str, reason: str = ""):
        self.filepath = filepath
        self.reason = reason
        message = f"Failed to load image: {filepath}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class InvalidFileFormatError(FileException):
    """Raised when a file has an invalid or unsupported format"""
    def __init__(self, filepath: str, expected_format: str = "", actual_format: str = ""):
        self.filepath = filepath
        self.expected_format = expected_format
        self.actual_format = actual_format
        message = f"Invalid file format: {filepath}"
        if expected_format:
            message += f" (expected {expected_format}"
            if actual_format:
                message += f", got {actual_format}"
            message += ")"
        super().__init__(message)


# UI-related exceptions

class UIException(PDFEditorException):
    """Base exception for UI-related errors"""
    pass


class DialogCancelledError(UIException):
    """Raised when a user cancels a dialog"""
    def __init__(self, dialog_type: str = ""):
        self.dialog_type = dialog_type
        message = "User cancelled dialog"
        if dialog_type:
            message = f"User cancelled {dialog_type} dialog"
        super().__init__(message)


class InvalidUIStateError(UIException):
    """Raised when the UI is in an invalid state for an operation"""
    def __init__(self, operation: str, reason: str):
        self.operation = operation
        self.reason = reason
        message = f"Cannot perform {operation}: {reason}"
        super().__init__(message)


# Validation exceptions

class ValidationException(PDFEditorException):
    """Base exception for validation errors"""
    pass


class EmptyTextError(ValidationException):
    """Raised when text input is empty but required"""
    def __init__(self, field_name: str = "text"):
        self.field_name = field_name
        message = f"{field_name.capitalize()} cannot be empty"
        super().__init__(message)


class ValueOutOfRangeError(ValidationException):
    """Raised when a value is outside the acceptable range"""
    def __init__(self, value_name: str, value: float, min_val: float, max_val: float):
        self.value_name = value_name
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        message = f"{value_name} must be between {min_val} and {max_val}, got {value}"
        super().__init__(message)


# Configuration exceptions

class ConfigException(PDFEditorException):
    """Base exception for configuration errors"""
    pass


class InvalidConfigError(ConfigException):
    """Raised when configuration is invalid"""
    def __init__(self, config_key: str, reason: str):
        self.config_key = config_key
        self.reason = reason
        message = f"Invalid configuration for '{config_key}': {reason}"
        super().__init__(message)


class MissingConfigError(ConfigException):
    """Raised when required configuration is missing"""
    def __init__(self, config_key: str):
        self.config_key = config_key
        message = f"Missing required configuration: '{config_key}'"
        super().__init__(message)

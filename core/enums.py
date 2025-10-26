"""
Core enumerations for the PDF Editor
"""

from enum import Enum


class EditMode(Enum):
    """Editing modes for the PDF editor"""
    TEXT = "text"
    IMAGE = "image"
    DOODLE = "doodle"


class ResizeEdge(Enum):
    """Enum for image/doodle resize edges"""
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"

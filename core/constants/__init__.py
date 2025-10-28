"""
Constants package for PDF Editor

This package organizes constants by domain for better maintainability.
All constants are re-exported here for backward compatibility.
"""

# Rendering constants
from core.constants.rendering import (
    BASE_SCALE,
    MIN_ZOOM,
    MAX_ZOOM,
    DEFAULT_ZOOM,
    ZOOM_SLIDER_MIN,
    ZOOM_SLIDER_MAX,
    ZOOM_SLIDER_DEFAULT,
    ZOOM_SLIDER_TICK_INTERVAL,
    ZOOM_SLIDER_WIDTH
)

# UI constants
from core.constants.ui import (
    EDGE_RESIZE_THRESHOLD,
    WINDOW_MARGIN,
    DECORATION_HEIGHT,
    DECORATION_WIDTH,
    MIN_ANNOTATION_SIZE,
    MIN_BUTTON_HEIGHT,
    BUTTON_HEIGHT_PADDING,
    DEFAULT_MENUBAR_HEIGHT
)

# Text constants
from core.constants.text import (
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    MIN_FONT_SIZE,
    MAX_FONT_SIZE,
    TEXT_ANNOTATION_WIDTH_PADDING,
    TEXT_ANNOTATION_HEIGHT_PADDING,
    TEXT_ANNOTATION_Y_OFFSET
)

# Drawing constants
from core.constants.drawing import (
    DEFAULT_PEN_WIDTH,
    MIN_PEN_WIDTH,
    MAX_PEN_WIDTH,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    DOODLE_PADDING
)

# Cursor constants
from core.constants.cursors import (
    TEXT_MODE_CURSOR,
    IMAGE_MODE_CURSOR,
    DOODLE_MODE_CURSOR
)

__all__ = [
    # Rendering
    'BASE_SCALE',
    'MIN_ZOOM',
    'MAX_ZOOM',
    'DEFAULT_ZOOM',
    'ZOOM_SLIDER_MIN',
    'ZOOM_SLIDER_MAX',
    'ZOOM_SLIDER_DEFAULT',
    'ZOOM_SLIDER_TICK_INTERVAL',
    'ZOOM_SLIDER_WIDTH',
    # UI
    'EDGE_RESIZE_THRESHOLD',
    'WINDOW_MARGIN',
    'DECORATION_HEIGHT',
    'DECORATION_WIDTH',
    'MIN_ANNOTATION_SIZE',
    'MIN_BUTTON_HEIGHT',
    'BUTTON_HEIGHT_PADDING',
    'DEFAULT_MENUBAR_HEIGHT',
    # Text
    'DEFAULT_FONT',
    'DEFAULT_FONT_SIZE',
    'MIN_FONT_SIZE',
    'MAX_FONT_SIZE',
    'TEXT_ANNOTATION_WIDTH_PADDING',
    'TEXT_ANNOTATION_HEIGHT_PADDING',
    'TEXT_ANNOTATION_Y_OFFSET',
    # Drawing
    'DEFAULT_PEN_WIDTH',
    'MIN_PEN_WIDTH',
    'MAX_PEN_WIDTH',
    'CANVAS_WIDTH',
    'CANVAS_HEIGHT',
    'DOODLE_PADDING',
    # Cursors
    'TEXT_MODE_CURSOR',
    'IMAGE_MODE_CURSOR',
    'DOODLE_MODE_CURSOR',
]

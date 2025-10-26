"""
Application constants and configuration values
"""

# Rendering
BASE_SCALE = 2.0  # Base DPI scaling for PDF rendering
MIN_ZOOM = 0.25   # 25%
MAX_ZOOM = 4.0    # 400%
DEFAULT_ZOOM = 1.0

# UI Dimensions
EDGE_RESIZE_THRESHOLD = 10  # pixels from edge to trigger resize
WINDOW_MARGIN = 50  # pixels margin from screen edge
DECORATION_HEIGHT = 40  # window title bar height
DECORATION_WIDTH = 20  # window border width
MIN_ANNOTATION_SIZE = 10  # minimum width/height for annotations

# Fonts
DEFAULT_FONT = "Arial"
DEFAULT_FONT_SIZE = 12
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 72

# Pen/Drawing
DEFAULT_PEN_WIDTH = 2
MIN_PEN_WIDTH = 1
MAX_PEN_WIDTH = 20

# Canvas
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
DOODLE_PADDING = 10

# Zoom Slider
ZOOM_SLIDER_MIN = 25  # 25%
ZOOM_SLIDER_MAX = 400  # 400%
ZOOM_SLIDER_DEFAULT = 100  # 100%
ZOOM_SLIDER_TICK_INTERVAL = 25
ZOOM_SLIDER_WIDTH = 200

# Button Heights
MIN_BUTTON_HEIGHT = 40
BUTTON_HEIGHT_PADDING = 10

# Menu Bar
DEFAULT_MENUBAR_HEIGHT = 25

# Text Annotation
TEXT_ANNOTATION_WIDTH_PADDING = 10
TEXT_ANNOTATION_HEIGHT_PADDING = 6
TEXT_ANNOTATION_Y_OFFSET = 4

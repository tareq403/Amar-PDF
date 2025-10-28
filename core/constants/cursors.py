"""
Cursor constants for different editing modes
"""

from PyQt5.QtCore import Qt

# Mode-specific cursors
TEXT_MODE_CURSOR = Qt.IBeamCursor           # | cursor for text editing
IMAGE_MODE_CURSOR = Qt.CrossCursor          # + cursor for precise image placement
DOODLE_MODE_CURSOR = Qt.PointingHandCursor  # Pointing hand cursor for drawing

"""
Data models for PDF Editor
"""

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import QRect


class TextAnnotation:
    """Represents a text annotation in draft mode"""
    def __init__(self, x, y, text, page_num, font_family="Arial", font_size=12,
                 bold=False, italic=False, underline=False, strikethrough=False):
        self.x = x
        self.y = y
        self.text = text
        self.page_num = page_num
        self.font_family = font_family
        self.font_size = font_size  # This is the actual PDF font size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.created_at_zoom = 1.0  # Will be set by the editor
        self.update_bounds()

    def update_bounds(self, zoom_level=1.0):
        """Calculate bounding box for the text at given zoom level"""
        font = self.get_qfont(zoom_level)
        metrics = QFontMetrics(font)
        self.width = metrics.horizontalAdvance(self.text) + 10
        self.height = metrics.height() + 6

    def get_qfont(self, zoom_level=1.0):
        """Get QFont object with all formatting applied for 2x scaled display with zoom"""
        # Font size needs to be 2x for the 2x scaled PDF display, then apply zoom
        display_font_size = self.font_size * 2 * zoom_level
        font = QFont(self.font_family, int(display_font_size))
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikethrough)
        return font

    def get_rect(self, current_zoom=1.0):
        """Get the bounding rectangle at given zoom level"""
        # Scale coordinates from creation zoom to current zoom
        zoom_ratio = current_zoom / self.created_at_zoom
        scaled_x = self.x * zoom_ratio
        scaled_y = self.y * zoom_ratio

        # Recalculate bounds for current zoom
        self.update_bounds(current_zoom)
        return QRect(int(scaled_x), int(scaled_y - self.height + 4), int(self.width), int(self.height))

    def contains_point(self, x, y, current_zoom=1.0):
        """Check if point is inside the annotation at current zoom"""
        return self.get_rect(current_zoom).contains(x, y)

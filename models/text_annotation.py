"""
Text annotation model
"""

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import QRect

from core.constants import (BASE_SCALE, DEFAULT_FONT, DEFAULT_FONT_SIZE,
                             TEXT_ANNOTATION_WIDTH_PADDING, TEXT_ANNOTATION_HEIGHT_PADDING,
                             TEXT_ANNOTATION_Y_OFFSET)
from models.annotation import Annotation


class TextAnnotation(Annotation):
    """Represents a text annotation in draft mode"""
    def __init__(self, x, y, text, page_num, font_family=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE,
                 bold=False, italic=False, underline=False, strikethrough=False):
        super().__init__(x, y, page_num)
        self.text = text
        self.font_family = font_family
        self.font_size = font_size  # This is the actual PDF font size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.update_bounds()

    def update_bounds(self, zoom_level=1.0):
        """Calculate bounding box for the text at given zoom level"""
        font = self.get_qfont(zoom_level)
        metrics = QFontMetrics(font)
        self.width = metrics.horizontalAdvance(self.text) + TEXT_ANNOTATION_WIDTH_PADDING
        self.height = metrics.height() + TEXT_ANNOTATION_HEIGHT_PADDING

    def get_qfont(self, zoom_level=1.0):
        """Get QFont object with all formatting applied for base scaled display with zoom"""
        # Font size needs to be BASE_SCALE for the scaled PDF display, then apply zoom
        display_font_size = self.font_size * BASE_SCALE * zoom_level
        font = QFont(self.font_family, int(display_font_size))
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikethrough)
        return font

    def get_rect(self, current_zoom=1.0):
        """Get the bounding rectangle at given zoom level"""
        # Scale coordinates from creation zoom to current zoom
        scaled_x, scaled_y = self._get_scaled_position(current_zoom)

        # Recalculate bounds for current zoom
        self.update_bounds(current_zoom)
        return QRect(int(scaled_x), int(scaled_y - self.height + TEXT_ANNOTATION_Y_OFFSET), int(self.width), int(self.height))

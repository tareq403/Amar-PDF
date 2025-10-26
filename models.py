"""
Data models for PDF Editor
"""

from abc import ABC, abstractmethod
from PyQt5.QtGui import QFont, QFontMetrics, QPixmap
from PyQt5.QtCore import QRect


class Annotation(ABC):
    """Base class for all annotation types"""
    def __init__(self, x, y, page_num):
        self.x = x
        self.y = y
        self.page_num = page_num
        self.created_at_zoom = 1.0  # Will be set by the editor

    @abstractmethod
    def get_rect(self, current_zoom=1.0):
        """Get the bounding rectangle at given zoom level"""
        pass

    def contains_point(self, x, y, current_zoom=1.0):
        """Check if point is inside the annotation at current zoom"""
        return self.get_rect(current_zoom).contains(x, y)

    def _get_zoom_ratio(self, current_zoom):
        """Helper to calculate zoom ratio"""
        return current_zoom / self.created_at_zoom

    def _get_scaled_position(self, current_zoom):
        """Helper to get scaled x, y coordinates"""
        zoom_ratio = self._get_zoom_ratio(current_zoom)
        scaled_x = self.x * zoom_ratio
        scaled_y = self.y * zoom_ratio
        return scaled_x, scaled_y


class TextAnnotation(Annotation):
    """Represents a text annotation in draft mode"""
    def __init__(self, x, y, text, page_num, font_family="Arial", font_size=12,
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
        scaled_x, scaled_y = self._get_scaled_position(current_zoom)

        # Recalculate bounds for current zoom
        self.update_bounds(current_zoom)
        return QRect(int(scaled_x), int(scaled_y - self.height + 4), int(self.width), int(self.height))


class ImageAnnotation(Annotation):
    """Represents an image annotation in draft mode"""
    def __init__(self, x, y, image_path, page_num, width=None, height=None):
        super().__init__(x, y, page_num)
        self.image_path = image_path

        # Load the image
        self.pixmap = QPixmap(image_path)

        # Set dimensions - default to original size
        if width is None or height is None:
            self.width = self.pixmap.width()
            self.height = self.pixmap.height()
        else:
            self.width = width
            self.height = height

    def get_rect(self, current_zoom=1.0):
        """Get the bounding rectangle at given zoom level"""
        # Scale coordinates from creation zoom to current zoom
        scaled_x, scaled_y = self._get_scaled_position(current_zoom)
        zoom_ratio = self._get_zoom_ratio(current_zoom)
        scaled_width = self.width * zoom_ratio
        scaled_height = self.height * zoom_ratio

        return QRect(int(scaled_x), int(scaled_y), int(scaled_width), int(scaled_height))

    def get_scaled_pixmap(self, current_zoom=1.0):
        """Get the pixmap scaled to current zoom level"""
        zoom_ratio = self._get_zoom_ratio(current_zoom)
        scaled_width = int(self.width * zoom_ratio)
        scaled_height = int(self.height * zoom_ratio)
        return self.pixmap.scaled(scaled_width, scaled_height)

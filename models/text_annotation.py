"""
Text annotation model
"""

from typing import TYPE_CHECKING, Tuple
from PyQt5.QtGui import QFont, QFontMetrics, QColor
from PyQt5.QtCore import QRect

from core.constants import (BASE_SCALE, DEFAULT_FONT, DEFAULT_FONT_SIZE,
                             TEXT_ANNOTATION_WIDTH_PADDING, TEXT_ANNOTATION_HEIGHT_PADDING,
                             TEXT_ANNOTATION_Y_OFFSET)
from models.annotation import Annotation

if TYPE_CHECKING:
    from models.text_format import TextFormat


class TextAnnotation(Annotation):
    """Represents a text annotation in draft mode"""
    def __init__(self, x, y, text, page_num, font_family=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE,
                 bold=False, italic=False, underline=False, strikethrough=False,
                 color: Tuple[int, int, int] = (0, 0, 0)):
        super().__init__(x, y, page_num)
        self.text = text
        self.font_family = font_family
        self.font_size = font_size  # This is the actual PDF font size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.color = color  # RGB tuple (r, g, b)
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

    def get_qcolor(self) -> QColor:
        """
        Get QColor object from RGB tuple.

        Returns:
            QColor object for Qt rendering
        """
        return QColor(*self.color)

    @classmethod
    def from_text_format(cls, x: float, y: float, page_num: int, text_format: 'TextFormat') -> 'TextAnnotation':
        """
        Create a TextAnnotation from a TextFormat object.

        This factory method provides a convenient way to create text annotations
        from the TextFormat data model returned by TextFormatDialog.

        Args:
            x: X coordinate on the PDF page
            y: Y coordinate on the PDF page
            page_num: Page number (0-indexed)
            text_format: TextFormat object containing text and formatting

        Returns:
            TextAnnotation instance with the specified format

        Example:
            >>> format = TextFormat(text="Hello", font_family="Arial", font_size=14, bold=True)
            >>> annotation = TextAnnotation.from_text_format(100, 200, 0, format)
        """
        return cls(
            x=x,
            y=y,
            text=text_format.text,
            page_num=page_num,
            font_family=text_format.font_family,
            font_size=text_format.font_size,
            bold=text_format.bold,
            italic=text_format.italic,
            underline=text_format.underline,
            strikethrough=text_format.strikethrough,
            color=text_format.color
        )

    @classmethod
    def simple(cls, x: float, y: float, text: str, page_num: int) -> 'TextAnnotation':
        """
        Create a simple text annotation with default formatting.

        Convenience factory method for creating text annotations with
        minimal parameters using default font and styling.

        Args:
            x: X coordinate on the PDF page
            y: Y coordinate on the PDF page
            text: Text content
            page_num: Page number (0-indexed)

        Returns:
            TextAnnotation instance with default formatting

        Example:
            >>> annotation = TextAnnotation.simple(100, 200, "Hello World", 0)
        """
        return cls(x, y, text, page_num)

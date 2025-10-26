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
        self.update_bounds()

    def update_bounds(self):
        """Calculate bounding box for the text"""
        font = self.get_qfont()
        metrics = QFontMetrics(font)
        self.width = metrics.horizontalAdvance(self.text) + 10
        self.height = metrics.height() + 6

    def get_qfont(self):
        """Get QFont object with all formatting applied for 2x scaled display"""
        # Font size needs to be 2x for the 2x scaled PDF display
        display_font_size = self.font_size * 2
        font = QFont(self.font_family, display_font_size)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikethrough)
        return font

    def get_rect(self):
        """Get the bounding rectangle"""
        return QRect(int(self.x), int(self.y - self.height + 4), int(self.width), int(self.height))

    def contains_point(self, x, y):
        """Check if point is inside the annotation"""
        return self.get_rect().contains(x, y)

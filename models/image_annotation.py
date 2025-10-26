"""
Image annotation model
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect

from models.annotation import Annotation


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

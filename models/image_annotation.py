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

    @classmethod
    def from_file(cls, x: float, y: float, image_path: str, page_num: int) -> 'ImageAnnotation':
        """
        Create an ImageAnnotation from an image file.

        Convenience factory method that uses the original image dimensions.

        Args:
            x: X coordinate on the PDF page
            y: Y coordinate on the PDF page
            image_path: Path to the image file
            page_num: Page number (0-indexed)

        Returns:
            ImageAnnotation instance with original image dimensions

        Raises:
            ImageLoadError: If the image file cannot be loaded

        Example:
            >>> annotation = ImageAnnotation.from_file(100, 200, "logo.png", 0)
        """
        return cls(x, y, image_path, page_num)

    @classmethod
    def from_file_with_size(cls, x: float, y: float, image_path: str, page_num: int,
                           width: int, height: int) -> 'ImageAnnotation':
        """
        Create an ImageAnnotation with specific dimensions.

        Factory method for creating image annotations with custom sizing.
        The image will be scaled to the specified dimensions.

        Args:
            x: X coordinate on the PDF page
            y: Y coordinate on the PDF page
            image_path: Path to the image file
            page_num: Page number (0-indexed)
            width: Desired width in pixels
            height: Desired height in pixels

        Returns:
            ImageAnnotation instance with specified dimensions

        Raises:
            ImageLoadError: If the image file cannot be loaded

        Example:
            >>> annotation = ImageAnnotation.from_file_with_size(100, 200, "logo.png", 0, 150, 100)
        """
        return cls(x, y, image_path, page_num, width, height)

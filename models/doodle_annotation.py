"""
Doodle annotation model
"""

from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import QRect, Qt
from typing import TYPE_CHECKING

from core.constants import DOODLE_PADDING
from models.annotation import Annotation

if TYPE_CHECKING:
    from models.drawing_data import DrawingData


class DoodleAnnotation(Annotation):
    """
    Represents a doodle/drawing annotation in draft mode.

    Args:
        x: X coordinate on the PDF page
        y: Y coordinate on the PDF page
        page_num: Page number this annotation belongs to
        drawing_data: DrawingData object containing all strokes
        width: Optional width override (calculated if not provided)
        height: Optional height override (calculated if not provided)
    """
    def __init__(self, x, y, page_num, drawing_data: 'DrawingData', width=None, height=None):
        super().__init__(x, y, page_num)
        self.drawing_data = drawing_data  # DrawingData object

        # Set dimensions - use provided dimensions or calculate from drawing
        if width is None or height is None:
            self.width, self.height = self._calculate_bounds()
        else:
            self.width = width
            self.height = height

        # Create pixmap from drawing data
        self.pixmap = self._create_pixmap()

    def _calculate_bounds(self):
        """Calculate bounding box from drawing data"""
        if not self.drawing_data or not self.drawing_data.strokes:
            return 100, 100  # Default size

        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for stroke in self.drawing_data.strokes:
            for x, y in stroke.points:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

        width = max(100, int(max_x - min_x + DOODLE_PADDING * 2))  # Add padding
        height = max(100, int(max_y - min_y + DOODLE_PADDING * 2))
        return width, height

    def _create_pixmap(self):
        """Create a pixmap from the drawing data"""
        # Create transparent image
        image = QImage(int(self.width), int(self.height), QImage.Format_ARGB32)
        image.fill(Qt.transparent)

        # Draw the strokes on the image
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)

        # Find bounds to offset drawing
        if self.drawing_data and self.drawing_data.strokes:
            min_x = min(x for stroke in self.drawing_data.strokes for x, y in stroke.points)
            min_y = min(y for stroke in self.drawing_data.strokes for x, y in stroke.points)
        else:
            min_x = min_y = 0

        for stroke in self.drawing_data.strokes:
            # Create QPen from stroke data
            pen = QPen(stroke.to_qcolor(), stroke.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)

            points = stroke.points
            for i in range(len(points) - 1):
                # Offset points to start from (0, 0)
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                painter.drawLine(
                    int(x1 - min_x + DOODLE_PADDING),
                    int(y1 - min_y + DOODLE_PADDING),
                    int(x2 - min_x + DOODLE_PADDING),
                    int(y2 - min_y + DOODLE_PADDING)
                )

        painter.end()
        return QPixmap.fromImage(image)

    def get_rect(self, current_zoom=1.0):
        """Get the bounding rectangle at given zoom level"""
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
    def from_drawing_data(cls, x: float, y: float, page_num: int,
                         drawing_data: 'DrawingData') -> 'DoodleAnnotation':
        """
        Create a DoodleAnnotation from DrawingData.

        Convenience factory method for creating doodle annotations with
        automatically calculated dimensions based on the drawing bounds.

        Args:
            x: X coordinate on the PDF page
            y: Y coordinate on the PDF page
            page_num: Page number (0-indexed)
            drawing_data: DrawingData object containing all strokes

        Returns:
            DoodleAnnotation instance with calculated dimensions

        Example:
            >>> drawing_data = DrawingData(strokes=[...])
            >>> annotation = DoodleAnnotation.from_drawing_data(100, 200, 0, drawing_data)
        """
        return cls(x, y, page_num, drawing_data)

    @classmethod
    def from_drawing_data_with_size(cls, x: float, y: float, page_num: int,
                                   drawing_data: 'DrawingData',
                                   width: int, height: int) -> 'DoodleAnnotation':
        """
        Create a DoodleAnnotation with specific dimensions.

        Factory method for creating doodle annotations with custom sizing.
        Use this when you want to override the automatically calculated bounds.

        Args:
            x: X coordinate on the PDF page
            y: Y coordinate on the PDF page
            page_num: Page number (0-indexed)
            drawing_data: DrawingData object containing all strokes
            width: Desired width in pixels
            height: Desired height in pixels

        Returns:
            DoodleAnnotation instance with specified dimensions

        Example:
            >>> drawing_data = DrawingData(strokes=[...])
            >>> annotation = DoodleAnnotation.from_drawing_data_with_size(
            ...     100, 200, 0, drawing_data, 300, 200
            ... )
        """
        return cls(x, y, page_num, drawing_data, width, height)

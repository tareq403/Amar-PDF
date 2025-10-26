"""
Doodle annotation model
"""

from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import QRect, Qt

from core.constants import DOODLE_PADDING
from models.annotation import Annotation


class DoodleAnnotation(Annotation):
    """Represents a doodle/drawing annotation in draft mode"""
    def __init__(self, x, y, page_num, drawing_data, width=None, height=None):
        super().__init__(x, y, page_num)
        self.drawing_data = drawing_data  # List of stroke paths

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
        if not self.drawing_data:
            return 100, 100  # Default size

        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for stroke in self.drawing_data:
            for point in stroke['points']:
                min_x = min(min_x, point.x())
                min_y = min(min_y, point.y())
                max_x = max(max_x, point.x())
                max_y = max(max_y, point.y())

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
        if self.drawing_data:
            min_x = min(point.x() for stroke in self.drawing_data for point in stroke['points'])
            min_y = min(point.y() for stroke in self.drawing_data for point in stroke['points'])
        else:
            min_x = min_y = 0

        for stroke in self.drawing_data:
            pen = stroke['pen']
            painter.setPen(pen)

            points = stroke['points']
            for i in range(len(points) - 1):
                # Offset points to start from (0, 0)
                p1 = points[i]
                p2 = points[i + 1]
                painter.drawLine(
                    int(p1.x() - min_x + DOODLE_PADDING),
                    int(p1.y() - min_y + DOODLE_PADDING),
                    int(p2.x() - min_x + DOODLE_PADDING),
                    int(p2.y() - min_y + DOODLE_PADDING)
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

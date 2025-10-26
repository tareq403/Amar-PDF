"""
Custom widgets for PDF Editor
"""

from PyQt5.QtWidgets import QLabel, QDialog
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

from dialogs import TextFormatDialog
from models import TextAnnotation, ImageAnnotation

# Import EditMode to avoid circular import
try:
    from enum import Enum
    class EditMode(Enum):
        TEXT = "text"
        IMAGE = "image"
        DOODLE = "doodle"
except:
    EditMode = None


class ResizeEdge(Enum):
    """Enum for image resize edges"""
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class PDFViewLabel(QLabel):
    """Custom label that can paint draft text and image annotations"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.annotations = []
        self.dragging_annotation = None
        self.drag_offset = QPoint(0, 0)
        self.zoom_level = 1.0  # Default zoom level
        self.resizing_annotation = None
        self.resize_edge = None  # Which edge is being resized: 'left', 'right', 'top', 'bottom'
        self.resize_start_pos = QPoint(0, 0)
        self.current_mode = None  # Will be set by parent editor
        self.setMouseTracking(True)  # Enable mouse tracking to update cursor on hover

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.annotations:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw each draft annotation with zoom level
        for annotation in self.annotations:
            rect = annotation.get_rect(self.zoom_level)

            if isinstance(annotation, TextAnnotation):
                # Draw dashed border
                pen = QPen(Qt.blue, 2, Qt.DashLine)
                painter.setPen(pen)
                painter.drawRect(rect)

                # Draw text with formatting at zoom level
                font = annotation.get_qfont(self.zoom_level)
                painter.setFont(font)
                pen = QPen(Qt.black)
                painter.setPen(pen)
                painter.drawText(rect.adjusted(5, 0, -5, 0), Qt.AlignLeft | Qt.AlignVCenter, annotation.text)

            elif isinstance(annotation, ImageAnnotation):
                # Draw the image
                scaled_pixmap = annotation.get_scaled_pixmap(self.zoom_level)
                painter.drawPixmap(rect.topLeft(), scaled_pixmap)

                # Draw dashed border
                pen = QPen(Qt.blue, 2, Qt.DashLine)
                painter.setPen(pen)
                painter.drawRect(rect)

        painter.end()

    def get_resize_edge(self, annotation, x, y):
        """Check if point is near an edge for resizing (only for images)"""
        if not isinstance(annotation, ImageAnnotation):
            return None

        rect = annotation.get_rect(self.zoom_level)
        edge_threshold = 10  # pixels from edge to trigger resize

        # Check each edge
        if abs(x - rect.left()) < edge_threshold and rect.top() <= y <= rect.bottom():
            return ResizeEdge.LEFT
        if abs(x - rect.right()) < edge_threshold and rect.top() <= y <= rect.bottom():
            return ResizeEdge.RIGHT
        if abs(y - rect.top()) < edge_threshold and rect.left() <= x <= rect.right():
            return ResizeEdge.TOP
        if abs(y - rect.bottom()) < edge_threshold and rect.left() <= x <= rect.right():
            return ResizeEdge.BOTTOM

        return None

    def mousePressEvent(self, event):
        # Check if clicking on existing annotation
        for annotation in self.annotations:
            if annotation.contains_point(event.x(), event.y(), self.zoom_level):
                # Check if near edge for resizing (images only)
                edge = self.get_resize_edge(annotation, event.x(), event.y())
                if edge:
                    self.resizing_annotation = annotation
                    self.resize_edge = edge
                    self.resize_start_pos = QPoint(event.x(), event.y())
                    event.accept()
                    return

                # Otherwise start dragging
                self.dragging_annotation = annotation
                # Calculate scaled position for drag offset
                zoom_ratio = self.zoom_level / annotation.created_at_zoom
                scaled_x = annotation.x * zoom_ratio
                scaled_y = annotation.y * zoom_ratio
                self.drag_offset = QPoint(event.x() - int(scaled_x), event.y() - int(scaled_y))
                event.accept()
                return

        # Pass to parent if not clicking on annotation
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing_annotation:
            # Handle image resizing - keep resize cursor
            zoom_ratio = self.zoom_level / self.resizing_annotation.created_at_zoom
            dx = event.x() - self.resize_start_pos.x()
            dy = event.y() - self.resize_start_pos.y()

            if self.resize_edge == ResizeEdge.RIGHT:
                new_width = self.resizing_annotation.width + dx / zoom_ratio
                if new_width > 10:  # Minimum width
                    self.resizing_annotation.width = new_width
                    self.resize_start_pos = QPoint(event.x(), event.y())
            elif self.resize_edge == ResizeEdge.LEFT:
                new_width = self.resizing_annotation.width - dx / zoom_ratio
                if new_width > 10:
                    self.resizing_annotation.x += dx / zoom_ratio
                    self.resizing_annotation.width = new_width
                    self.resize_start_pos = QPoint(event.x(), event.y())
            elif self.resize_edge == ResizeEdge.BOTTOM:
                new_height = self.resizing_annotation.height + dy / zoom_ratio
                if new_height > 10:  # Minimum height
                    self.resizing_annotation.height = new_height
                    self.resize_start_pos = QPoint(event.x(), event.y())
            elif self.resize_edge == ResizeEdge.TOP:
                new_height = self.resizing_annotation.height - dy / zoom_ratio
                if new_height > 10:
                    self.resizing_annotation.y += dy / zoom_ratio
                    self.resizing_annotation.height = new_height
                    self.resize_start_pos = QPoint(event.x(), event.y())

            self.update()
            event.accept()
        elif self.dragging_annotation:
            # Set closed hand cursor while dragging
            self.setCursor(Qt.ClosedHandCursor)

            # Update position in the original zoom space
            zoom_ratio = self.zoom_level / self.dragging_annotation.created_at_zoom
            new_x = (event.x() - self.drag_offset.x()) / zoom_ratio
            new_y = (event.y() - self.drag_offset.y()) / zoom_ratio
            self.dragging_annotation.x = new_x
            self.dragging_annotation.y = new_y
            self.update()
            event.accept()
        else:
            # Update cursor based on hover position and mode
            cursor_set = False

            # Check for image resize edges first (highest priority)
            for annotation in self.annotations:
                if isinstance(annotation, ImageAnnotation):
                    edge = self.get_resize_edge(annotation, event.x(), event.y())
                    if edge in (ResizeEdge.LEFT, ResizeEdge.RIGHT):
                        self.setCursor(Qt.SizeHorCursor)
                        cursor_set = True
                        break
                    elif edge in (ResizeEdge.TOP, ResizeEdge.BOTTOM):
                        self.setCursor(Qt.SizeVerCursor)
                        cursor_set = True
                        break

            # If not over resize edge, set cursor based on mode
            if not cursor_set:
                if EditMode and self.current_mode == EditMode.TEXT:
                    self.setCursor(Qt.IBeamCursor)  # Text cursor (I-beam)
                else:
                    self.setCursor(Qt.ArrowCursor)  # Default arrow cursor

            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.resizing_annotation:
            self.resizing_annotation = None
            self.resize_edge = None
            # Reset cursor based on current mode after resizing
            if EditMode and self.current_mode == EditMode.TEXT:
                self.setCursor(Qt.IBeamCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
            event.accept()
        elif self.dragging_annotation:
            self.dragging_annotation = None
            # Reset cursor based on current mode after dragging
            if EditMode and self.current_mode == EditMode.TEXT:
                self.setCursor(Qt.IBeamCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Check if double-clicking on existing text annotation to edit
        for annotation in self.annotations:
            if isinstance(annotation, TextAnnotation) and annotation.contains_point(event.x(), event.y(), self.zoom_level):
                dialog = TextFormatDialog(
                    self,
                    initial_text=annotation.text,
                    initial_font=annotation.font_family,
                    initial_size=annotation.font_size,
                    initial_bold=annotation.bold,
                    initial_italic=annotation.italic,
                    initial_underline=annotation.underline,
                    initial_strikethrough=annotation.strikethrough
                )
                if dialog.exec_() == QDialog.Accepted:
                    values = dialog.get_values()
                    if values['text']:
                        annotation.text = values['text']
                        annotation.font_family = values['font_family']
                        annotation.font_size = values['font_size']
                        annotation.bold = values['bold']
                        annotation.italic = values['italic']
                        annotation.underline = values['underline']
                        annotation.strikethrough = values['strikethrough']
                        annotation.update_bounds()
                        self.update()
                event.accept()
                return

        super().mouseDoubleClickEvent(event)

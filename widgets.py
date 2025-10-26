"""
Custom widgets for PDF Editor
"""

from PyQt5.QtWidgets import QLabel, QDialog
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

from dialogs import TextFormatDialog


class PDFViewLabel(QLabel):
    """Custom label that can paint draft text annotations"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.annotations = []
        self.dragging_annotation = None
        self.drag_offset = QPoint(0, 0)
        self.zoom_level = 1.0  # Default zoom level

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.annotations:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw each draft annotation with zoom level
        for annotation in self.annotations:
            # Draw dashed border
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            rect = annotation.get_rect(self.zoom_level)
            painter.drawRect(rect)

            # Draw text with formatting at zoom level
            font = annotation.get_qfont(self.zoom_level)
            painter.setFont(font)
            pen = QPen(Qt.black)
            painter.setPen(pen)
            painter.drawText(rect.adjusted(5, 0, -5, 0), Qt.AlignLeft | Qt.AlignVCenter, annotation.text)

        painter.end()

    def mousePressEvent(self, event):
        # Check if clicking on existing annotation
        for annotation in self.annotations:
            if annotation.contains_point(event.x(), event.y(), self.zoom_level):
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
        if self.dragging_annotation:
            # Update position in the original zoom space
            zoom_ratio = self.zoom_level / self.dragging_annotation.created_at_zoom
            new_x = (event.x() - self.drag_offset.x()) / zoom_ratio
            new_y = (event.y() - self.drag_offset.y()) / zoom_ratio
            self.dragging_annotation.x = new_x
            self.dragging_annotation.y = new_y
            self.update()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragging_annotation:
            self.dragging_annotation = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Check if double-clicking on existing annotation to edit
        for annotation in self.annotations:
            if annotation.contains_point(event.x(), event.y(), self.zoom_level):
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

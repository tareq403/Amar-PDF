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

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.annotations:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw each draft annotation
        for annotation in self.annotations:
            # Draw dashed border
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            rect = annotation.get_rect()
            painter.drawRect(rect)

            # Draw text with formatting
            font = annotation.get_qfont()
            painter.setFont(font)
            pen = QPen(Qt.black)
            painter.setPen(pen)
            painter.drawText(rect.adjusted(5, 0, -5, 0), Qt.AlignLeft | Qt.AlignVCenter, annotation.text)

        painter.end()

    def mousePressEvent(self, event):
        # Check if clicking on existing annotation
        for annotation in self.annotations:
            if annotation.contains_point(event.x(), event.y()):
                self.dragging_annotation = annotation
                self.drag_offset = QPoint(event.x() - int(annotation.x), event.y() - int(annotation.y))
                event.accept()
                return

        # Pass to parent if not clicking on annotation
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging_annotation:
            self.dragging_annotation.x = event.x() - self.drag_offset.x()
            self.dragging_annotation.y = event.y() - self.drag_offset.y()
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
            if annotation.contains_point(event.x(), event.y()):
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

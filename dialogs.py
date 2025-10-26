"""
Dialog classes for PDF Editor
"""

from PyQt5.QtWidgets import (QDialog, QLineEdit, QFontComboBox, QSpinBox,
                             QCheckBox, QDialogButtonBox, QFormLayout,
                             QGroupBox, QVBoxLayout, QLabel, QHBoxLayout,
                             QPushButton, QColorDialog)
from PyQt5.QtGui import QFont, QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint


class TextFormatDialog(QDialog):
    """Dialog for text input with font formatting options"""
    def __init__(self, parent=None, initial_text="", initial_font="Arial", initial_size=12,
                 initial_bold=False, initial_italic=False, initial_underline=False, initial_strikethrough=False):
        super().__init__(parent)
        self.setWindowTitle("Text Format")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Text input
        form_layout = QFormLayout()
        self.text_edit = QLineEdit(initial_text)
        form_layout.addRow("Text:", self.text_edit)

        # Font selection
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(initial_font))
        form_layout.addRow("Font:", self.font_combo)

        # Font size
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(6)
        self.size_spin.setMaximum(72)
        self.size_spin.setValue(initial_size)
        form_layout.addRow("Size:", self.size_spin)

        layout.addLayout(form_layout)

        # Text decorations
        decoration_group = QGroupBox("Text Decorations")
        decoration_layout = QVBoxLayout()

        self.bold_check = QCheckBox("Bold")
        self.bold_check.setChecked(initial_bold)
        decoration_layout.addWidget(self.bold_check)

        self.italic_check = QCheckBox("Italic")
        self.italic_check.setChecked(initial_italic)
        decoration_layout.addWidget(self.italic_check)

        self.underline_check = QCheckBox("Underline")
        self.underline_check.setChecked(initial_underline)
        decoration_layout.addWidget(self.underline_check)

        self.strikethrough_check = QCheckBox("Strikethrough")
        self.strikethrough_check.setChecked(initial_strikethrough)
        decoration_layout.addWidget(self.strikethrough_check)

        decoration_group.setLayout(decoration_layout)
        layout.addWidget(decoration_group)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_values(self):
        """Return the text and formatting options"""
        return {
            'text': self.text_edit.text(),
            'font_family': self.font_combo.currentFont().family(),
            'font_size': self.size_spin.value(),
            'bold': self.bold_check.isChecked(),
            'italic': self.italic_check.isChecked(),
            'underline': self.underline_check.isChecked(),
            'strikethrough': self.strikethrough_check.isChecked()
        }


class DrawingCanvas(QLabel):
    """Canvas widget for free-hand drawing"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: white; border: 1px solid gray;")

        self.drawing = False
        self.current_stroke = []
        self.strokes = []  # List of stroke dictionaries
        self.current_pen = QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        # Create canvas pixmap
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.setPixmap(self.canvas)

    def set_pen_color(self, color):
        """Set the drawing pen color"""
        self.current_pen.setColor(color)

    def set_pen_width(self, width):
        """Set the drawing pen width"""
        self.current_pen.setWidth(width)

    def clear_canvas(self):
        """Clear the entire canvas"""
        self.strokes = []
        self.canvas.fill(Qt.white)
        self.setPixmap(self.canvas)

    def mousePressEvent(self, event):
        """Start drawing a new stroke"""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.current_stroke = [event.pos()]

    def mouseMoveEvent(self, event):
        """Continue drawing the current stroke"""
        if self.drawing and event.buttons() & Qt.LeftButton:
            self.current_stroke.append(event.pos())

            # Draw on canvas
            painter = QPainter(self.canvas)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(self.current_pen)

            if len(self.current_stroke) >= 2:
                painter.drawLine(self.current_stroke[-2], self.current_stroke[-1])

            painter.end()
            self.setPixmap(self.canvas)

    def mouseReleaseEvent(self, event):
        """Finish the current stroke"""
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            if self.current_stroke:
                # Save the stroke
                self.strokes.append({
                    'points': self.current_stroke.copy(),
                    'pen': QPen(self.current_pen)  # Copy the pen
                })
                self.current_stroke = []

    def get_drawing_data(self):
        """Return the stroke data"""
        return self.strokes


class DoodleDialog(QDialog):
    """Dialog for free-hand drawing/doodling"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Draw Doodle")
        self.setMinimumSize(700, 550)

        layout = QVBoxLayout(self)

        # Drawing canvas
        self.canvas = DrawingCanvas()
        layout.addWidget(self.canvas)

        # Controls
        controls_layout = QHBoxLayout()

        # Color button
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)
        controls_layout.addWidget(self.color_button)

        # Pen width
        controls_layout.addWidget(QLabel("Pen Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(1)
        self.width_spin.setMaximum(20)
        self.width_spin.setValue(2)
        self.width_spin.valueChanged.connect(self.canvas.set_pen_width)
        controls_layout.addWidget(self.width_spin)

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.canvas.clear_canvas)
        controls_layout.addWidget(clear_button)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.current_color = Qt.black

    def choose_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor(self.current_color, self, "Choose Pen Color")
        if color.isValid():
            self.current_color = color
            self.canvas.set_pen_color(color)
            self.color_button.setStyleSheet(f"background-color: {color.name()};")

    def get_drawing_data(self):
        """Return the drawing data"""
        return self.canvas.get_drawing_data()

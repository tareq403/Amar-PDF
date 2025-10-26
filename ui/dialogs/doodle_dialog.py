"""
Doodle/drawing dialog
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QHBoxLayout,
                             QPushButton, QColorDialog, QSpinBox, QDialogButtonBox)
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint

from core.constants import (CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_PEN_WIDTH,
                             MIN_PEN_WIDTH, MAX_PEN_WIDTH)


class DrawingCanvas(QLabel):
    """Canvas widget for free-hand drawing"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.setStyleSheet("background-color: white; border: 1px solid gray;")

        self.drawing = False
        self.current_stroke = []
        self.strokes = []  # List of stroke dictionaries
        self.current_pen = QPen(Qt.black, DEFAULT_PEN_WIDTH, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

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
        self.width_spin.setMinimum(MIN_PEN_WIDTH)
        self.width_spin.setMaximum(MAX_PEN_WIDTH)
        self.width_spin.setValue(DEFAULT_PEN_WIDTH)
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

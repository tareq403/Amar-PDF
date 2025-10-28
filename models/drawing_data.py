"""
Drawing data model for doodle strokes
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint

from core.constants import DEFAULT_PEN_WIDTH, MIN_PEN_WIDTH, MAX_PEN_WIDTH


@dataclass
class Stroke:
    """
    Represents a single stroke in a doodle drawing.

    A stroke is a continuous line drawn by the user, consisting of multiple
    points and styling information (color, width).

    Attributes:
        points: List of (x, y) coordinate tuples representing the stroke path
        color: RGB color tuple (r, g, b) where each value is 0-255
        width: Pen width in pixels
    """
    points: List[Tuple[int, int]]
    color: Tuple[int, int, int] = (0, 0, 0)  # Black by default
    width: int = DEFAULT_PEN_WIDTH

    def __post_init__(self):
        """Validate stroke data after initialization"""
        # Validate points list
        if not self.points:
            raise ValueError("Stroke must have at least one point")

        # Validate each point is a tuple of 2 integers
        for point in self.points:
            if not isinstance(point, tuple) or len(point) != 2:
                raise ValueError(f"Invalid point format: {point}. Expected (x, y) tuple")

        # Validate pen width
        if not (MIN_PEN_WIDTH <= self.width <= MAX_PEN_WIDTH):
            raise ValueError(
                f"Pen width must be between {MIN_PEN_WIDTH} and {MAX_PEN_WIDTH}, "
                f"got {self.width}"
            )

        # Validate color (RGB values 0-255)
        if len(self.color) != 3:
            raise ValueError(f"Color must be RGB tuple (r, g, b), got {self.color}")

        for component in self.color:
            if not (0 <= component <= 255):
                raise ValueError(
                    f"Color components must be 0-255, got {component} in {self.color}"
                )

    def is_valid(self) -> bool:
        """Check if the stroke has valid data"""
        return len(self.points) >= 2  # Need at least 2 points to draw a line

    @classmethod
    def from_qpoints(cls, qpoints: List[QPoint], qcolor: QColor, width: int) -> 'Stroke':
        """
        Create a Stroke from Qt objects.

        Args:
            qpoints: List of QPoint objects
            qcolor: QColor object
            width: Pen width in pixels

        Returns:
            Stroke instance with converted data
        """
        points = [(p.x(), p.y()) for p in qpoints]
        color = (qcolor.red(), qcolor.green(), qcolor.blue())
        return cls(points=points, color=color, width=width)

    def to_qpoints(self) -> List[QPoint]:
        """
        Convert stroke points to QPoint objects.

        Returns:
            List of QPoint objects for Qt rendering
        """
        return [QPoint(x, y) for x, y in self.points]

    def to_qcolor(self) -> QColor:
        """
        Convert stroke color to QColor object.

        Returns:
            QColor object for Qt rendering
        """
        return QColor(*self.color)


@dataclass
class DrawingData:
    """
    Container for all strokes in a doodle drawing.

    This class encapsulates a complete drawing consisting of multiple strokes,
    providing a type-safe alternative to dictionary/list-based data passing.

    Attributes:
        strokes: List of Stroke objects representing the complete drawing
    """
    strokes: List[Stroke] = field(default_factory=list)

    def __post_init__(self):
        """Validate drawing data after initialization"""
        # Ensure all strokes are Stroke instances
        for stroke in self.strokes:
            if not isinstance(stroke, Stroke):
                raise TypeError(f"All strokes must be Stroke instances, got {type(stroke)}")

    def is_valid(self) -> bool:
        """
        Check if the drawing has valid content.

        Returns:
            True if drawing has at least one valid stroke, False otherwise
        """
        return len(self.strokes) > 0 and any(stroke.is_valid() for stroke in self.strokes)

    def add_stroke(self, stroke: Stroke) -> None:
        """
        Add a stroke to the drawing.

        Args:
            stroke: Stroke object to add
        """
        if not isinstance(stroke, Stroke):
            raise TypeError(f"Expected Stroke instance, got {type(stroke)}")
        self.strokes.append(stroke)

    def clear(self) -> None:
        """Remove all strokes from the drawing"""
        self.strokes.clear()

    def stroke_count(self) -> int:
        """
        Get the number of strokes in the drawing.

        Returns:
            Number of strokes
        """
        return len(self.strokes)

    @classmethod
    def from_dict_list(cls, dict_list: List[dict]) -> 'DrawingData':
        """
        Create DrawingData from the old dictionary format.

        This method provides backward compatibility with the old format where
        strokes were stored as dictionaries with 'points' and 'pen' keys.

        Args:
            dict_list: List of dictionaries with 'points' (list of QPoint)
                      and 'pen' (QPen) keys

        Returns:
            DrawingData instance with converted strokes
        """
        strokes = []
        for stroke_dict in dict_list:
            qpoints = stroke_dict['points']
            qpen = stroke_dict['pen']

            stroke = Stroke.from_qpoints(
                qpoints=qpoints,
                qcolor=qpen.color(),
                width=qpen.width()
            )
            strokes.append(stroke)

        return cls(strokes=strokes)

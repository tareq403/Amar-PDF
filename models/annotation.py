"""
Base annotation class
"""

from abc import ABC, abstractmethod


class Annotation(ABC):
    """Base class for all annotation types"""
    def __init__(self, x, y, page_num):
        self.x = x
        self.y = y
        self.page_num = page_num
        self.created_at_zoom = 1.0  # Will be set by the editor

    @abstractmethod
    def get_rect(self, current_zoom=1.0):
        """Get the bounding rectangle at given zoom level"""
        pass

    def contains_point(self, x, y, current_zoom=1.0):
        """Check if point is inside the annotation at current zoom"""
        return self.get_rect(current_zoom).contains(x, y)

    def _get_zoom_ratio(self, current_zoom):
        """Helper to calculate zoom ratio"""
        return current_zoom / self.created_at_zoom

    def _get_scaled_position(self, current_zoom):
        """Helper to get scaled x, y coordinates"""
        zoom_ratio = self._get_zoom_ratio(current_zoom)
        scaled_x = self.x * zoom_ratio
        scaled_y = self.y * zoom_ratio
        return scaled_x, scaled_y

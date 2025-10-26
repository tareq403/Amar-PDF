"""
Helper utility functions
"""

from PyQt5.QtCore import QRect


def create_rect(x, y, width, height):
    """
    Create a QRect with integer coordinates
    
    Args:
        x: X coordinate (will be converted to int)
        y: Y coordinate (will be converted to int)
        width: Width (will be converted to int)
        height: Height (will be converted to int)
    
    Returns:
        QRect: Rectangle with integer coordinates
    """
    return QRect(int(x), int(y), int(width), int(height))


def scale_coordinate(value, zoom_ratio):
    """
    Scale a coordinate by a zoom ratio
    
    Args:
        value: The coordinate value to scale
        zoom_ratio: The zoom ratio to apply
    
    Returns:
        float: Scaled coordinate
    """
    return value * zoom_ratio


def pdf_to_screen_coords(pdf_x, pdf_y, base_scale, zoom):
    """
    Convert PDF coordinates to screen coordinates
    
    Args:
        pdf_x: PDF X coordinate
        pdf_y: PDF Y coordinate
        base_scale: Base rendering scale (typically 2.0)
        zoom: Current zoom level
    
    Returns:
        tuple: (screen_x, screen_y)
    """
    screen_x = pdf_x * base_scale * zoom
    screen_y = pdf_y * base_scale * zoom
    return screen_x, screen_y


def screen_to_pdf_coords(screen_x, screen_y, base_scale, zoom):
    """
    Convert screen coordinates to PDF coordinates
    
    Args:
        screen_x: Screen X coordinate
        screen_y: Screen Y coordinate
        base_scale: Base rendering scale (typically 2.0)
        zoom: Current zoom level
    
    Returns:
        tuple: (pdf_x, pdf_y)
    """
    pdf_x = screen_x / (base_scale * zoom)
    pdf_y = screen_y / (base_scale * zoom)
    return pdf_x, pdf_y

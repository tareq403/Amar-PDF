"""
Application configuration and settings
Contains runtime configurable settings (as opposed to constants.py which has fixed values)
"""

class Config:
    """Application configuration settings"""
    
    # Default window dimensions
    DEFAULT_WINDOW_WIDTH = 800
    DEFAULT_WINDOW_HEIGHT = 600
    DEFAULT_WINDOW_X = 100
    DEFAULT_WINDOW_Y = 100
    
    # File paths
    DEFAULT_SAVE_FILENAME = "edited.pdf"
    
    # Supported file formats
    SUPPORTED_IMAGE_FORMATS = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
    SUPPORTED_PDF_FORMATS = "PDF Files (*.pdf)"
    
    # Debug mode
    DEBUG = False
    
    @classmethod
    def get_default_window_geometry(cls):
        """Get default window geometry as tuple"""
        return (cls.DEFAULT_WINDOW_X, cls.DEFAULT_WINDOW_Y, 
                cls.DEFAULT_WINDOW_WIDTH, cls.DEFAULT_WINDOW_HEIGHT)

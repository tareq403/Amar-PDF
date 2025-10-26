"""
Models package for PDF Editor
Contains all annotation model classes
"""

from models.annotation import Annotation
from models.text_annotation import TextAnnotation
from models.image_annotation import ImageAnnotation
from models.doodle_annotation import DoodleAnnotation

__all__ = ['Annotation', 'TextAnnotation', 'ImageAnnotation', 'DoodleAnnotation']

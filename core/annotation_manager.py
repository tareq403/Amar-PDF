"""
Annotation management for PDF Editor
"""

from typing import List, Optional
from models import Annotation


class AnnotationManager:
    """
    Manages all annotations in the PDF Editor.

    This class provides a centralized way to manage annotations across pages,
    handle filtering by page, and maintain annotation state.

    Attributes:
        annotations: List of all annotations in the document
    """

    def __init__(self):
        """Initialize the annotation manager with an empty annotation list"""
        self.annotations: List[Annotation] = []

    def add_annotation(self, annotation: Annotation) -> None:
        """
        Add an annotation to the manager.

        Args:
            annotation: Annotation object to add

        Raises:
            TypeError: If annotation is not an Annotation instance
        """
        if not isinstance(annotation, Annotation):
            raise TypeError(f"Expected Annotation instance, got {type(annotation)}")

        self.annotations.append(annotation)

    def remove_annotation(self, annotation: Annotation) -> bool:
        """
        Remove an annotation from the manager.

        Args:
            annotation: Annotation object to remove

        Returns:
            True if annotation was found and removed, False otherwise
        """
        try:
            self.annotations.remove(annotation)
            return True
        except ValueError:
            return False

    def get_annotations_for_page(self, page_num: int) -> List[Annotation]:
        """
        Get all annotations for a specific page.

        Args:
            page_num: Page number (0-indexed)

        Returns:
            List of annotations on the specified page
        """
        return [a for a in self.annotations if a.page_num == page_num]

    def get_annotations_by_type(self, annotation_type: type) -> List[Annotation]:
        """
        Get all annotations of a specific type.

        Args:
            annotation_type: Type of annotation to filter by (e.g., TextAnnotation)

        Returns:
            List of annotations matching the specified type

        Example:
            >>> from models import TextAnnotation
            >>> text_annotations = manager.get_annotations_by_type(TextAnnotation)
        """
        return [a for a in self.annotations if isinstance(a, annotation_type)]

    def clear_all(self) -> None:
        """Remove all annotations"""
        self.annotations.clear()

    def clear_page(self, page_num: int) -> int:
        """
        Remove all annotations from a specific page.

        Args:
            page_num: Page number (0-indexed)

        Returns:
            Number of annotations removed
        """
        initial_count = len(self.annotations)
        self.annotations = [a for a in self.annotations if a.page_num != page_num]
        return initial_count - len(self.annotations)

    def update_page_numbers(self, page_mapping: List[int]) -> None:
        """
        Update annotation page numbers based on a page mapping.

        This is useful when pages are reordered or deleted.

        Args:
            page_mapping: List where index is new page number and value is old page number

        Example:
            >>> # If pages were reordered from [0,1,2,3] to [2,0,1,3]
            >>> manager.update_page_numbers([2,0,1,3])
        """
        # Create reverse mapping (old page -> new page)
        reverse_mapping = {}
        for new_page, old_page in enumerate(page_mapping):
            reverse_mapping[old_page] = new_page

        # Update annotations that are still in the document
        updated_annotations = []
        for annotation in self.annotations:
            if annotation.page_num in reverse_mapping:
                annotation.page_num = reverse_mapping[annotation.page_num]
                updated_annotations.append(annotation)

        self.annotations = updated_annotations

    def has_annotations(self) -> bool:
        """
        Check if there are any annotations.

        Returns:
            True if annotations exist, False otherwise
        """
        return len(self.annotations) > 0

    def count(self) -> int:
        """
        Get the total number of annotations.

        Returns:
            Number of annotations
        """
        return len(self.annotations)

    def count_for_page(self, page_num: int) -> int:
        """
        Get the number of annotations on a specific page.

        Args:
            page_num: Page number (0-indexed)

        Returns:
            Number of annotations on the page
        """
        return len(self.get_annotations_for_page(page_num))

    def find_annotation_at_point(self, x: float, y: float, page_num: int,
                                  zoom_level: float = 1.0) -> Optional[Annotation]:
        """
        Find an annotation at a specific point on a page.

        Args:
            x: X coordinate
            y: Y coordinate
            page_num: Page number (0-indexed)
            zoom_level: Current zoom level

        Returns:
            First annotation found at the point, or None if no annotation exists

        Note:
            If multiple annotations overlap at the point, returns the first match.
            Consider the order of annotations in the list (typically last added is on top).
        """
        page_annotations = self.get_annotations_for_page(page_num)

        # Check in reverse order (last added is on top)
        for annotation in reversed(page_annotations):
            if annotation.contains_point(x, y, zoom_level):
                return annotation

        return None

    def get_all_annotations(self) -> List[Annotation]:
        """
        Get all annotations in the manager.

        Returns:
            Copy of the annotations list

        Note:
            Returns a copy to prevent external modifications.
            Use add_annotation() and remove_annotation() to modify.
        """
        return self.annotations.copy()

    def __len__(self) -> int:
        """
        Get the number of annotations.

        Returns:
            Number of annotations

        Example:
            >>> len(manager)
            5
        """
        return len(self.annotations)

    def __repr__(self) -> str:
        """
        String representation of the annotation manager.

        Returns:
            String showing annotation count
        """
        return f"AnnotationManager(annotations={len(self.annotations)})"

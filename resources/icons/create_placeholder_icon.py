#!/usr/bin/env python3
"""
Create a simple placeholder icon for PDF Editor

This creates a basic icon with a document shape and text.
Replace this with your own professional icon design.

Requirements:
    pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    exit(1)


def create_placeholder_icon():
    """Create a simple placeholder icon"""

    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (0, 120, 212, 255)  # Blue
    doc_color = (255, 255, 255, 255)  # White
    fold_color = (200, 200, 200, 255)  # Light gray

    # Padding
    padding = 150

    # Document shape (rounded rectangle)
    doc_left = padding
    doc_top = padding
    doc_right = size - padding
    doc_bottom = size - padding

    # Background circle
    draw.ellipse([50, 50, size-50, size-50], fill=bg_color)

    # Document rectangle with rounded corners
    corner_radius = 50
    doc_rect = [doc_left, doc_top, doc_right, doc_bottom]

    # Draw rounded rectangle for document
    draw.rounded_rectangle(doc_rect, corner_radius, fill=doc_color)

    # Draw folded corner
    fold_size = 120
    fold_points = [
        (doc_right - fold_size, doc_top),  # Top right - fold_size
        (doc_right, doc_top + fold_size),  # Right side + fold_size
        (doc_right - fold_size, doc_top + fold_size),  # Corner point
    ]
    draw.polygon(fold_points, fill=fold_color)

    # Draw lines to represent text
    line_left = doc_left + 80
    line_right = doc_right - 120
    line_width = 8
    line_color = (0, 120, 212, 200)

    for i in range(4):
        line_y = doc_top + 250 + (i * 80)
        draw.rectangle(
            [line_left, line_y, line_right, line_y + line_width],
            fill=line_color
        )

    # Draw edit symbol (pencil-like)
    pencil_size = 180
    pencil_x = doc_left + 150
    pencil_y = doc_bottom - 230

    # Pencil body
    pencil_points = [
        (pencil_x, pencil_y + pencil_size),
        (pencil_x + 40, pencil_y + pencil_size),
        (pencil_x + 20, pencil_y),
    ]
    draw.polygon(pencil_points, fill=(255, 165, 0, 255))  # Orange

    # Pencil tip
    tip_points = [
        (pencil_x + 8, pencil_y + pencil_size),
        (pencil_x + 32, pencil_y + pencil_size),
        (pencil_x + 20, pencil_y + pencil_size + 20),
    ]
    draw.polygon(tip_points, fill=(50, 50, 50, 255))  # Dark gray

    # Save
    img.save('icon_base.png', 'PNG')
    print("✓ Placeholder icon created: icon_base.png")
    print("\nThis is a simple placeholder icon.")
    print("For production, consider:")
    print("  - Using a professional design tool (Figma, Illustrator)")
    print("  - Hiring a designer on Fiverr/99designs")
    print("  - Using AI image generation (DALL-E, Midjourney)")
    print("  - Downloading from icon libraries (with proper license)")


if __name__ == "__main__":
    create_placeholder_icon()

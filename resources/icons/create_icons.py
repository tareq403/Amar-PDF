#!/usr/bin/env python3
"""
Icon Generator Script for PDF Editor

This script helps convert a base PNG icon to formats needed for all platforms.

Requirements:
    pip install Pillow

Usage:
    1. Place your base icon as 'icon_base.png' (1024x1024 recommended)
    2. Run: python create_icons.py
    3. Icons will be generated:
       - icon.png (Linux)
       - icon.ico (Windows)
       - For macOS .icns: Use online converter or iconutil on macOS

Note: This script creates PNG and ICO. For best macOS support,
      use iconutil on macOS or an online converter for ICNS format.
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


def create_icons(base_image_path="icon_base.png"):
    """Create all required icon formats from base image"""

    # Check if base image exists
    if not os.path.exists(base_image_path):
        print(f"ERROR: Base image '{base_image_path}' not found!")
        print("\nPlease create a base icon image:")
        print("  - Name: icon_base.png")
        print("  - Size: 1024x1024 pixels (or 512x512)")
        print("  - Format: PNG with transparency")
        print("  - Place in: resources/icons/")
        return False

    try:
        # Load base image
        print(f"Loading base image: {base_image_path}")
        img = Image.open(base_image_path)

        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            print("Converting image to RGBA mode...")
            img = img.convert('RGBA')

        print(f"Base image size: {img.size}")

        # Create Linux PNG (512x512)
        print("\n1. Creating icon.png (Linux)...")
        linux_icon = img.resize((512, 512), Image.Resampling.LANCZOS)
        linux_icon.save('icon.png', 'PNG')
        print("   ✓ icon.png created (512x512)")

        # Create Windows ICO (multi-size)
        print("\n2. Creating icon.ico (Windows)...")
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        ico_images = []

        for size in sizes:
            ico_img = img.resize(size, Image.Resampling.LANCZOS)
            ico_images.append(ico_img)

        # Save as ICO with multiple sizes
        ico_images[0].save(
            'icon.ico',
            format='ICO',
            sizes=[(img.width, img.height) for img in ico_images]
        )
        print(f"   ✓ icon.ico created (multi-size: {', '.join(f'{s[0]}x{s[1]}' for s in sizes)})")

        # macOS ICNS instructions
        print("\n3. Creating icon.icns (macOS)...")
        print("   ⚠ ICNS format requires additional tools.")
        print("   Options:")
        print("   a) Use online converter:")
        print("      - Visit: https://iconverticons.com/online/")
        print("      - Upload: icon.png")
        print("      - Download: icon.icns")
        print("   b) Use iconutil on macOS:")
        print("      - Run: ./create_icns.sh (see instructions below)")
        print("   c) Use png2icns (install: brew install libicns):")
        print("      - Run: png2icns icon.icns icon.png")

        # Create helper script for macOS
        create_icns_script()

        print("\n" + "="*60)
        print("SUCCESS! Icons created:")
        print("  ✓ icon.png (512x512) - Ready for Linux")
        print("  ✓ icon.ico (multi-size) - Ready for Windows")
        print("  ⚠ icon.icns - Requires additional step (see above)")
        print("="*60)

        return True

    except Exception as e:
        print(f"\nERROR: Failed to create icons: {e}")
        return False


def create_icns_script():
    """Create a helper bash script for macOS ICNS generation"""
    script_content = """#!/bin/bash
# Helper script to create macOS ICNS icon
# Requires: macOS (uses iconutil)
# Usage: ./create_icns.sh

set -e

if [ ! -f "icon.png" ]; then
    echo "ERROR: icon.png not found!"
    echo "Run create_icons.py first."
    exit 1
fi

echo "Creating iconset directory..."
mkdir -p icon.iconset

echo "Generating all required sizes..."
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

echo "Converting to ICNS..."
iconutil -c icns icon.iconset

echo "Cleaning up..."
rm -rf icon.iconset

echo "✓ icon.icns created successfully!"
"""

    with open('create_icns.sh', 'w') as f:
        f.write(script_content)

    # Make executable
    os.chmod('create_icns.sh', 0o755)
    print("\n   Helper script created: create_icns.sh")


def main():
    """Main entry point"""
    print("="*60)
    print("PDF Editor Icon Generator")
    print("="*60)

    # Check for base image
    base_image = "icon_base.png"

    if not os.path.exists(base_image):
        print("\nNo base image found. Checking for alternative names...")
        alternatives = ["icon.png", "logo.png", "app_icon.png"]

        for alt in alternatives:
            if os.path.exists(alt):
                base_image = alt
                print(f"Found: {alt}")
                break
        else:
            print("\nNo icon found. Please create one first.")
            print("\nQuick start:")
            print("1. Create a 1024x1024 PNG icon")
            print("2. Name it 'icon_base.png'")
            print("3. Place in resources/icons/")
            print("4. Run this script again")
            return

    # Create icons
    if create_icons(base_image):
        print("\nNext steps:")
        print("1. If on macOS, run: ./create_icns.sh")
        print("   OR use online converter for icon.icns")
        print("2. Verify all three icon files exist:")
        print("   - icon.png")
        print("   - icon.ico")
        print("   - icon.icns")
        print("3. Commit and push to repository")
        print("4. Build executables will use these icons automatically")


if __name__ == "__main__":
    main()

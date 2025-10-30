#!/bin/bash
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

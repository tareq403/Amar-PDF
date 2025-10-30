"""
User Guide Dialog
Displays comprehensive guide for using the PDF Editor
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextBrowser,
                             QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.styles import USER_GUIDE_STYLESHEET


class UserGuideDialog(QDialog):
    """Dialog displaying user guide with all features and usage instructions"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Amar PDF - User Guide")
        self.setMinimumSize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)

        # Set light background for the entire dialog (for dark mode compatibility)
        self.setStyleSheet(USER_GUIDE_STYLESHEET)

        # Create text browser for displaying guide
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.setHtml(self.get_guide_content())

        # Set font
        font = QFont()
        font.setPointSize(11)
        self.text_browser.setFont(font)

        layout.addWidget(self.text_browser)

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.setMinimumWidth(100)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def get_guide_content(self):
        """Returns the HTML content for the user guide"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                    line-height: 1.6;
                    padding: 20px;
                    color: #333;
                }
                h1 {
                    color: #0078d4;
                    border-bottom: 3px solid #0078d4;
                    padding-bottom: 10px;
                    margin-top: 0;
                }
                h2 {
                    color: #0078d4;
                    margin-top: 30px;
                    margin-bottom: 15px;
                }
                h3 {
                    color: #333;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                .feature {
                    background-color: #f5f5f5;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border-left: 4px solid #0078d4;
                }
                .steps {
                    margin-left: 20px;
                }
                .steps li {
                    margin: 8px 0;
                }
                .shortcut {
                    background-color: #e8e8e8;
                    padding: 2px 8px;
                    border-radius: 3px;
                    font-family: "Courier New", monospace;
                    font-size: 0.9em;
                }
                .tip {
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 10px;
                    margin: 15px 0;
                }
                .mode-badge {
                    background-color: #0078d4;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 3px;
                    font-size: 0.85em;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>📄 Amar PDF - User Guide</h1>

            <p><strong>Welcome to Amar PDF!</strong> This guide will help you make the most of all features.</p>

            <h2>🚀 Getting Started</h2>

            <div class="feature">
                <h3>Opening a PDF</h3>
                <ul class="steps">
                    <li>Click anywhere on the welcome screen, or</li>
                    <li>Use <span class="shortcut">File → Open PDF</span>, or</li>
                    <li>Press <span class="shortcut">Cmd+O</span> (Mac) / <span class="shortcut">Ctrl+O</span> (Windows/Linux)</li>
                </ul>
            </div>

            <h2>📋 Main Interface</h2>

            <div class="feature">
                <h3>Navigation Controls (Bottom Panel)</h3>
                <ul class="steps">
                    <li><strong>&lt; / &gt; Buttons:</strong> Navigate between pages</li>
                    <li><strong>Zoom Slider:</strong> Adjust zoom level from 25% to 400%</li>
                    <li><strong>Page Counter:</strong> Shows current page and total pages (e.g., "Page 1/5")</li>
                    <li><strong>See All Pages:</strong> View all pages at once for reordering or deletion</li>
                </ul>
            </div>

            <h2>✏️ Editing Modes</h2>

            <p>The toolbar has three editing modes. Select one before clicking on the PDF:</p>

            <div class="feature">
                <h3><span class="mode-badge">T</span> Text Mode (Default)</h3>
                <p><strong>Cursor:</strong> I-beam (|) cursor for text editing</p>
                <ul class="steps">
                    <li>Click on the PDF where you want to add text</li>
                    <li>Enter your text in the dialog</li>
                    <li>Choose formatting:
                        <ul>
                            <li>Font family (Arial, Times New Roman, Courier, etc.)</li>
                            <li>Font size (6pt - 72pt)</li>
                            <li>Style: Bold, Italic, Underline, Strikethrough</li>
                            <li>Text color (click color button to choose)</li>
                        </ul>
                    </li>
                    <li>Click <strong>OK</strong> to add the text</li>
                    <li>Text appears with blue dashed border (draft mode)</li>
                </ul>

                <div class="tip">
                    <strong>💡 Tip:</strong> Double-click existing text to edit it!
                </div>
            </div>

            <div class="feature">
                <h3><span class="mode-badge">🖼️</span> Image Mode</h3>
                <p><strong>Cursor:</strong> Crosshair (+) for precise placement</p>
                <ul class="steps">
                    <li>Click the Image mode button in toolbar</li>
                    <li>Click on the PDF where you want to place the image</li>
                    <li>Select an image file (PNG, JPG, JPEG, BMP, GIF)</li>
                    <li>Image appears with blue dashed border</li>
                    <li><strong>Resize:</strong> Drag the edges</li>
                    <li><strong>Move:</strong> Drag the center</li>
                </ul>
            </div>

            <div class="feature">
                <h3><span class="mode-badge">✎</span> Doodle Mode</h3>
                <p><strong>Cursor:</strong> Pointing hand for drawing</p>
                <ul class="steps">
                    <li>Click the Doodle mode button in toolbar</li>
                    <li>Click on the PDF where you want to draw</li>
                    <li>In the drawing dialog:
                        <ul>
                            <li>Draw freely with mouse or stylus</li>
                            <li>Click <strong>Choose Color</strong> to change pen color</li>
                            <li>Adjust <strong>Pen Width</strong> (1-20 pixels)</li>
                            <li>Click <strong>Clear</strong> to start over</li>
                        </ul>
                    </li>
                    <li>Click <strong>OK</strong> to place on PDF</li>
                    <li><strong>Resize:</strong> Drag the edges</li>
                    <li><strong>Move:</strong> Drag the center</li>
                </ul>
            </div>

            <h2>💾 Saving Your Work</h2>

            <div class="feature">
                <h3>Save PDF with Annotations</h3>
                <ul class="steps">
                    <li>Use <span class="shortcut">File → Save</span>, or</li>
                    <li>Press <span class="shortcut">Cmd+S</span> (Mac) / <span class="shortcut">Ctrl+S</span> (Windows/Linux), or</li>
                    <li>Click the <strong>💾 Save</strong> button in toolbar</li>
                    <li>Choose save location and filename</li>
                    <li>All annotations are <strong>permanently applied</strong> to the PDF</li>
                </ul>

                <div class="tip">
                    <strong>⚠️ Note:</strong> After saving, draft annotations are cleared. Your changes are now permanent in the saved PDF.
                </div>
            </div>

            <h2>📑 Page Management</h2>

            <div class="feature">
                <h3>View All Pages</h3>
                <ul class="steps">
                    <li>Click <strong>See All Pages</strong> button at bottom</li>
                    <li>All pages displayed vertically with thumbnails</li>
                    <li>Current view is a <strong>preview</strong> - changes not applied until confirmed</li>
                </ul>
            </div>

            <div class="feature">
                <h3>Reorder Pages</h3>
                <ul class="steps">
                    <li>In All Pages window, <strong>drag and drop</strong> pages</li>
                    <li>Pages are numbered automatically</li>
                    <li>Click <strong>Confirm</strong> to apply changes</li>
                    <li>Click <strong>Cancel</strong> to discard changes</li>
                </ul>

                <div class="tip">
                    <strong>💡 Smart Feature:</strong> Annotations automatically move with their pages!
                </div>
            </div>

            <div class="feature">
                <h3>Delete Pages</h3>
                <ul class="steps">
                    <li>In All Pages window, click red <strong>Delete</strong> button on any page</li>
                    <li>Confirmation dialog appears</li>
                    <li>Click <strong>Yes</strong> to delete, <strong>No</strong> to cancel</li>
                    <li>Click <strong>Confirm</strong> to apply deletion</li>
                </ul>

                <div class="tip">
                    <strong>⚠️ Warning:</strong> Annotations on deleted pages will be permanently removed!
                </div>
            </div>

            <h2>🔗 Merging PDFs</h2>

            <div class="feature">
                <h3>Link Another PDF</h3>
                <ul class="steps">
                    <li>Open a PDF document first</li>
                    <li>Use <span class="shortcut">File → Link another PDF</span>, or</li>
                    <li>Click the <strong>🔗 Link PDF</strong> button in toolbar</li>
                    <li>Select the PDF file to merge</li>
                    <li>All pages from selected PDF are appended to current document</li>
                    <li>Success dialog shows page count details</li>
                    <li>Remember to <strong>Save</strong> to keep the merged PDF</li>
                </ul>

                <div class="tip">
                    <strong>💡 Tip:</strong> Existing annotations remain on their original pages after merging.
                </div>
            </div>

            <h2>🔍 Zooming</h2>

            <div class="feature">
                <h3>Zoom Controls</h3>
                <ul class="steps">
                    <li>Drag the <strong>zoom slider</strong> at the bottom</li>
                    <li>Range: 25% to 400%</li>
                    <li>Current zoom level shown next to slider (e.g., "100%")</li>
                    <li>Window automatically resizes to fit content</li>
                    <li>All annotations scale correctly with zoom</li>
                </ul>

                <div class="tip">
                    <strong>💡 Smart Feature:</strong> Annotations maintain their exact position when you zoom!
                </div>
            </div>

            <h2>⌨️ Keyboard Shortcuts</h2>

            <div class="feature">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><span class="shortcut">Cmd+O</span> / <span class="shortcut">Ctrl+O</span></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">Open PDF</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><span class="shortcut">Cmd+S</span> / <span class="shortcut">Ctrl+S</span></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">Save PDF</td>
                    </tr>
                </table>
            </div>

            <h2>💡 Tips & Tricks</h2>

            <div class="feature">
                <h3>Working with Annotations</h3>
                <ul class="steps">
                    <li><strong>Move:</strong> Click and drag annotation to new position</li>
                    <li><strong>Resize (Images/Doodles):</strong> Hover over edge until resize cursor appears, then drag</li>
                    <li><strong>Edit Text:</strong> Double-click text annotation to edit content and formatting</li>
                    <li><strong>Delete:</strong> Not yet implemented - create new PDF without unwanted annotations</li>
                </ul>
            </div>

            <div class="feature">
                <h3>Cursor Indicators</h3>
                <ul class="steps">
                    <li><strong>I-beam (|):</strong> Text mode - click to add text</li>
                    <li><strong>Crosshair (+):</strong> Image mode - click to place image</li>
                    <li><strong>Pointing hand:</strong> Doodle mode - click to draw</li>
                    <li><strong>Open hand:</strong> Over draggable annotation</li>
                    <li><strong>Closed hand:</strong> Dragging annotation</li>
                    <li><strong>Horizontal/Vertical arrows:</strong> Resize edges</li>
                </ul>
            </div>

            <div class="feature">
                <h3>Best Practices</h3>
                <ul class="steps">
                    <li><strong>Save often:</strong> Use Cmd+S / Ctrl+S frequently</li>
                    <li><strong>Test zoom:</strong> Check annotations at different zoom levels</li>
                    <li><strong>Preview before saving:</strong> Verify all annotations look correct</li>
                    <li><strong>Backup originals:</strong> Keep a copy of original PDFs</li>
                    <li><strong>Use See All Pages:</strong> Great for overview before final save</li>
                </ul>
            </div>

            <h2>❓ Common Questions</h2>

            <div class="feature">
                <h3>Can I undo an annotation?</h3>
                <p>Before saving: Simply close and reopen the PDF. Unsaved annotations are discarded.</p>
                <p>After saving: Annotations are permanent. Open the original PDF to start over.</p>
            </div>

            <div class="feature">
                <h3>Why are there dashed blue borders?</h3>
                <p>This is "draft mode" - annotations are previewed but not yet saved to the PDF.
                Borders disappear after saving.</p>
            </div>

            <div class="feature">
                <h3>Can I edit PDF text content?</h3>
                <p>No, this editor adds annotations <em>on top of</em> existing PDF content.
                The original PDF content cannot be modified.</p>
            </div>

            <div class="feature">
                <h3>What happens to annotations when I merge PDFs?</h3>
                <p>Existing annotations stay on their original page numbers.
                New pages from merged PDF are added without annotations.</p>
            </div>

            <h2>🎯 Quick Reference</h2>

            <div class="feature">
                <h3>Toolbar Buttons (Left to Right)</h3>
                <ul class="steps">
                    <li><strong>💾</strong> - Save PDF with annotations</li>
                    <li><strong>🔗</strong> - Link another PDF (merge)</li>
                    <li><strong>T</strong> - Text mode (toggle)</li>
                    <li><strong>🖼️</strong> - Image mode (toggle)</li>
                    <li><strong>✎</strong> - Doodle mode (toggle)</li>
                    <li><strong>?</strong> - User Guide (this window)</li>
                </ul>
            </div>

            <hr style="margin: 30px 0;">

            <p style="text-align: center; color: #666;">
                <strong>Need more help?</strong><br>
                Check the README.md file in the project directory for additional information.
            </p>

        </body>
        </html>
        """

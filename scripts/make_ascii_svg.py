#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import sys

def image_to_ascii_svg(image_path, width=100, char_height=1.2):
    """Convert prepped image to ASCII art SVG with self-typing animation."""
    
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load {image_path}")
        sys.exit(1)
    
    # Resize to character grid
    aspect = img.shape[0] / img.shape[1]
    height = int(width * aspect * 0.55)
    img_resized = cv2.resize(img, (width, height))
    
    # ASCII ramp: bright -> dark
    ramp = " .`:-=+*cs#%@"
    
    # Map pixels to characters
    ascii_grid = []
    for row in img_resized:
        line = ""
        for pixel in row:
            idx = int((pixel / 255.0) * (len(ramp) - 1))
            line += ramp[idx]
        ascii_grid.append(line)
    
    print(f"ASCII grid: {width}x{height}")
    
    # Build SVG with CSS animation
    char_width = 7
    line_height = int(char_height * 14)
    svg_width = width * char_width + 20
    svg_height = height * line_height + 20
    
    svg_content = f"""<svg viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .ascii-line {
        font-family: monospace;
        font-size: 12px;
        fill: #999;
        white-space: pre;
        opacity: 0;
        animation: fadeIn 0.4s ease-out forwards;
      }
      @keyframes fadeIn {
        to { opacity: 1; }
      }
    </style>
  </defs>
"""
    
    for i, line in enumerate(ascii_grid):
        delay = i * 0.03
        y = 15 + i * line_height
        svg_content += f'  <text x="10" y="{y}" class="ascii-line" style="animation-delay: {delay}s">{line}</text>\n'
    
    svg_content += '</svg>'
    
    with open("avi-ascii.svg", "w") as f:
        f.write(svg_content)
    
    print("Saved: avi-ascii.svg")

if __name__ == "__main__":
    image_to_ascii_svg("source-prepped.png")
#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from PIL import Image

def prep_photo(input_path):
    """Prep a photo for ASCII conversion: remove background, boost contrast, composite on white."""
    
    # Load image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not load {input_path}")
        sys.exit(1)
    
    h, w = img.shape[:2]
    print(f"Loaded image: {w}x{h}")
    
    # Try to remove background with rembg
    try:
        from rembg import remove
        print("Removing background...")
        img_pil = Image.open(input_path)
        img_nobg = remove(img_pil)
        img = cv2.cvtColor(np.array(img_nobg), cv2.COLOR_RGBA2BGRA)
    except ImportError:
        print("rembg not installed, skipping background removal")
    except Exception as e:
        print(f"Background removal failed: {e}, continuing...")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE for local contrast boost
    print("Boosting local contrast...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Composite onto pure white
    result = np.full((enhanced.shape[0], enhanced.shape[1]), 255, dtype=np.uint8)
    result = cv2.addWeighted(result, 0.7, enhanced, 0.3, 0)
    
    # Save
    cv2.imwrite("source-prepped.png", result)
    print("Saved: source-prepped.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)
    prep_photo(sys.argv[1])
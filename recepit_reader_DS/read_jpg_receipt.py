import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import sys
import os

def enhance_receipt_image(image_path):
    """Enhance JPG receipt image for better OCR"""
    
    # Read image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding (helps with uneven lighting)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Denoise
    denoised = cv2.medianBlur(thresh, 3)
    
    # Save enhanced version
    enhanced_path = "enhanced_temp.jpg"
    cv2.imwrite(enhanced_path, denoised)
    
    return enhanced_path

def read_receipt_jpg(image_path):
    """Read receipt from JPG with enhancement"""
    
    print(f"📸 Processing JPG receipt: {image_path}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File '{image_path}' not found!")
        return None
    
    try:
        # First try with original
        print("🔄 Attempting to read original image...")
        img = Image.open(image_path)
        text_original = pytesseract.image_to_string(img)
        
        # If original gives very little text, try enhancement
        if len(text_original.strip()) < 50:
            print("🔄 Original image gave little text, applying enhancements...")
            enhanced_path = enhance_receipt_image(image_path)
            img_enhanced = Image.open(enhanced_path)
            text = pytesseract.image_to_string(img_enhanced)
            os.remove(enhanced_path)  # Clean up temp file
        else:
            text = text_original
        
        return text
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=== JPG Receipt Reader (Enhanced) ===\n")
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to your receipt JPG: ")
        image_path = image_path.strip('"').strip("'")
    
    text = read_receipt_jpg(image_path)
    
    if text:
        print("\n✅ Success! Extracted text:\n")
        print("="*60)
        print(text)
        print("="*60)
        
        # Save to file
        output_file = "receipt_text.txt"
        with open(output_file, 'w') as f:
            f.write(text)
        print(f"\n💾 Text saved to: {output_file}")
        
        # Show some statistics
        lines = text.split('\n')
        print(f"\n📊 Statistics:")
        print(f"   - Total lines: {len(lines)}")
        print(f"   - Characters: {len(text)}")
        print(f"   - Words: {len(text.split())}")
        
    else:
        print("\n❌ Failed to read the receipt. Try:")
        print("   - Taking a clearer photo")
        print("   - Ensuring good lighting")
        print("   - Holding the camera steady")

if __name__ == "__main__":
    main()

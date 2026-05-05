import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import sys
import os

def preprocess_image(image_path, method='auto'):
    """Apply various preprocessing methods to improve OCR"""
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    results = {}
    
    # Method 1: Grayscale + Threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    results['threshold'] = thresh
    
    # Method 2: Adaptive Threshold (good for uneven lighting)
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
    results['adaptive'] = adaptive
    
    # Method 3: Denoise + Sharpen
    denoised = cv2.medianBlur(gray, 3)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    results['sharpened'] = sharpened
    
    # Method 4: Scale up (makes small text more readable)
    height, width = gray.shape
    scaled = cv2.resize(gray, (width*2, height*2), interpolation=cv2.INTER_CUBIC)
    _, scaled_thresh = cv2.threshold(scaled, 150, 255, cv2.THRESH_BINARY)
    results['scaled'] = scaled_thresh
    
    # Method 5: Morphological operations (remove noise)
    kernel = np.ones((1,1), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    results['morphed'] = morphed
    
    return results

def extract_text_with_methods(image_path):
    """Try multiple preprocessing methods and return best result"""
    
    print("🔍 Analyzing receipt...")
    
    # First, try original
    print("  📸 Testing original image...")
    original = Image.open(image_path)
    original_text = pytesseract.image_to_string(original)
    
    # Preprocess with different methods
    print("  🎨 Trying preprocessing methods...")
    processed = preprocess_image(image_path)
    
    if processed is None:
        return original_text
    
    results = {}
    results['original'] = original_text
    
    # Test each method
    for method_name, img_array in processed.items():
        print(f"     - {method_name}...")
        temp_path = f"/tmp/receipt_{method_name}.png"
        cv2.imwrite(temp_path, img_array)
        pil_img = Image.open(temp_path)
        text = pytesseract.image_to_string(pil_img)
        results[method_name] = text
        os.remove(temp_path)
    
    # Find the best result (longest text usually means most detected)
    best_method = max(results, key=lambda x: len(results[x].strip()))
    best_text = results[best_method]
    
    print(f"\n✓ Best method: {best_method}")
    print(f"  Characters extracted: {len(best_text)}")
    
    return best_text, best_method

def extract_receipt_data(text):
    """Try to extract key information from receipt text"""
    
    import re
    
    data = {
        'total': None,
        'date': None,
        'store': None,
        'tax': None,
        'items': []
    }
    
    # Look for total amount (various formats)
    total_patterns = [
        r'TOTAL\s*[$]?\s*(\d+\.?\d*)',
        r'Total\s*[$]?\s*(\d+\.?\d*)',
        r'AMOUNT\s*[$]?\s*(\d+\.?\d*)',
        r'Amount\s*[$]?\s*(\d+\.?\d*)',
        r'BALANCE\s*[$]?\s*(\d+\.?\d*)',
        r'Balance\s*[$]?\s*(\d+\.?\d*)',
        r'DUE\s*[$]?\s*(\d+\.?\d*)',
        r'Due\s*[$]?\s*(\d+\.?\d*)',
        r'=+\s*[$]?\s*(\d+\.?\d*)',
        r'GRAND TOTAL\s*[$]?\s*(\d+\.?\d*)'
    ]
    
    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['total'] = float(match.group(1))
            break
    
    # Look for date
    date_patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}',
        r'\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
        r'(\d{1,2}/\d{1,2}/\d{2,4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['date'] = match.group(1)
            break
    
    # Look for store name (usually first few lines)
    lines = text.split('\n')
    for i in range(min(5, len(lines))):
        line = lines[i].strip()
        if line and len(line) > 5 and len(line) < 50:
            # Skip lines with only numbers or common words
            if not re.match(r'^[\d\s\.\$-]+$', line):
                data['store'] = line
                break
    
    # Look for tax
    tax_patterns = [
        r'TAX\s*[$]?\s*(\d+\.?\d*)',
        r'Tax\s*[$]?\s*(\d+\.?\d*)',
        r'SALES TAX\s*[$]?\s*(\d+\.?\d*)'
    ]
    
    for pattern in tax_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['tax'] = float(match.group(1))
            break
    
    return data

def main():
    print("="*60)
    print("ADVANCED RECEIPT READER")
    print("="*60)
    
    # Get image path
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("\n📁 Enter receipt image path: ")
    
    image_path = image_path.strip().strip("'").strip('"')
    
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    # Extract text
    text, method = extract_text_with_methods(image_path)
    
    # Extract key data
    data = extract_receipt_data(text)
    
    # Display results
    print("\n" + "="*60)
    print("📄 EXTRACTED INFORMATION")
    print("="*60)
    
    if data['store']:
        print(f"🏪 Store: {data['store']}")
    else:
        print("🏪 Store: Not detected")
    
    if data['date']:
        print(f"📅 Date: {data['date']}")
    else:
        print("📅 Date: Not detected")
    
    if data['total']:
        print(f"💰 Total: ${data['total']:.2f}")
    else:
        print("💰 Total: Not detected")
    
    if data['tax']:
        print(f"📊 Tax: ${data['tax']:.2f}")
    
    print("\n" + "="*60)
    print("📝 FULL EXTRACTED TEXT")
    print("="*60)
    print(text)
    print("="*60)
    
    # Save everything
    with open('receipt_full_text.txt', 'w') as f:
        f.write(text)
    
    import json
    with open('receipt_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Saved:")
    print(f"   - Full text: receipt_full_text.txt")
    print(f"   - Extracted data: receipt_data.json")
    
    # Quality assessment
    if len(text.strip()) < 100:
        print("\n⚠️  Low text quality detected!")
        print("\n📸 Tips for better results:")
        print("   1. Take photo in GOOD LIGHTING (natural light works best)")
        print("   2. Hold camera PARALLEL to receipt (not at angle)")
        print("   3. Keep phone STEADY (use both hands)")
        print("   4. Avoid GLARE on glossy receipts")
        print("   5. Scan with FLATBED SCANNER if possible")
        print("   6. Try using a RECEIPT SCANNING APP first, then export")
    elif data['total']:
        print("\n✅ Good quality! Successfully extracted total amount.")
    else:
        print("\n📸 Moderate quality detected. Try improving lighting for better results.")

if __name__ == "__main__":
    main()
import cv2
import pytesseract
import numpy as np
from PIL import Image
import re
import os
from thefuzz import fuzz # Ensure you ran: pip install thefuzz

def preprocess_for_ocr(image_path):
    """
    Cleans the image to make text stand out.
    """
    # 1. Load in Grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not find {image_path}")

    # 2. Resizing (Enlarging small receipts helps OCR accuracy)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 3. Denoising
    img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)

    # 4. Adaptive Thresholding (Creates high contrast)
    cleaned = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Save for your inspection
    cv2.imwrite("final_clean_receipt.jpg", cleaned)
    return cleaned

def extract_smart_total(raw_text):
    """
    Algorithm: Fuzzy String Matching + Regex
    Goal: Find 'Total' even if it's hidden by borders or typos.
    """
    lines = raw_text.split('\n')
    extracted_total = "Not found"
    best_match_line = ""
    
    # We look for these keywords using fuzzy matching
    target_keywords = ["TOTAL", "AMOUNT DUE", "BALANCE", "NET"]

    for line in lines:
        clean_line = line.strip().upper()
        if not clean_line: continue

        # Check this line against each keyword
        for keyword in target_keywords:
            # Score similarity (0 to 100)
            # partial_ratio is great for finding 'TOTAL' inside '| TOTAL |'
            similarity = fuzz.partial_ratio(clean_line, keyword)

            if similarity > 80: # High confidence match
                # Now use Regex to find the price in this line
                price_match = re.search(r'\d+[.,]\d{2}', clean_line)
                if price_match:
                    extracted_total = price_match.group()
                    best_match_line = clean_line
                    return extracted_total, best_match_line

    return extracted_total, best_match_line

# --- Main Execution ---
TARGET = "test_receipt.jpg"

if os.path.exists(TARGET):
    try:
        # Step 1: Clean the image
        processed_img = preprocess_for_ocr(TARGET)
        
        # Step 2: OCR (psm 6 is best for uniform text blocks)
        raw_text = pytesseract.image_to_string(processed_img, config='--psm 6')
        
        # Step 3: Fuzzy Logic Extraction
        total, line_found = extract_smart_total(raw_text)
        
        print("\n" + "="*40)
        print("🧾 SMART RECEIPT SCANNER")
        print("="*40)
        if total != "Not found":
            print(f"✅ SUCCESS")
            print(f"Line Identified: {line_found}")
            print(f"Total Amount:    ${total}")
        else:
            print(f"❌ TOTAL NOT DETECTED")
            print("Try checking 'final_clean_receipt.jpg' to see if text is legible.")
        print("="*40)

    except Exception as e:
        print(f"Algorithm Error: {e}")
else:
    print(f"File {TARGET} not found.")
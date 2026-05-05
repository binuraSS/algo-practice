import pytesseract
import cv2
from PIL import Image
import sys

print("Step 1: Checking imports...")
print("✓ All imports successful")

print("\nStep 2: Checking Tesseract...")
try:
    version = pytesseract.get_tesseract_version()
    print(f"✓ Tesseract version: {version}")
except Exception as e:
    print(f"✗ Tesseract not found: {e}")
    print("Please make sure Tesseract is installed with: brew install tesseract")
    sys.exit(1)

print("\n✓ Setup is complete! Ready to build the receipt reader.")

# Create a simple test image (a black square with white text)
from PIL import ImageDraw, ImageFont
img = Image.new('RGB', (400, 100), color='black')
d = ImageDraw.Draw(img)
d.text((10, 10), "TEST RECEIPT", fill='white')
d.text((10, 40), "Total: $42.99", fill='white')
img.save('test_receipt.png')

print("\nCreated test image: test_receipt.png")

# Try to read it
text = pytesseract.image_to_string(img)
print(f"\nOCR Test Result: '{text.strip()}'")



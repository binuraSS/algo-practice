import os
import glob

print("="*50)
print("Image Finder Diagnostic Tool")
print("="*50)

# Show current directory
current_dir = os.getcwd()
print(f"\n📍 Current directory: {current_dir}")

# List all files in current directory
print(f"\n📁 All files in current directory:")
files = os.listdir('.')
for file in files:
    print(f"   - {file}")

# Look for image files
print(f"\n🖼️  Looking for image files...")
image_extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG', '*.bmp', '*.tiff']

found_images = []
for ext in image_extensions:
    images = glob.glob(ext)
    for img in images:
        found_images.append(img)
        print(f"   ✓ Found: {img}")

if not found_images:
    print(f"   ❌ No image files found in current directory!")
    print(f"\n💡 Tips:")
    print(f"   1. Make sure your image is in: {current_dir}")
    print(f"   2. Check if the file name has spaces or special characters")
    print(f"   3. Try moving the image to this folder")
else:
    print(f"\n✅ Found {len(found_images)} image(s)")
    print(f"\n📝 To read one of these images, use:")
    for img in found_images:
        print(f"   python3 simple_reader.py")
        print(f"   Then enter: {img}")
import numpy as np
from PIL import Image

def detect_fruit_by_color(img):
    img_array = np.array(img)
    
    avg_r = img_array[:,:,0].mean()
    avg_g = img_array[:,:,1].mean()
    avg_b = img_array[:,:,2].mean()
    
    print(f"Average colors - R: {avg_r:.2f}, G: {avg_g:.2f}, B: {avg_b:.2f}")
    
    if avg_r > avg_g and avg_r > avg_b and avg_r > 100:
        return "Apple (Red dominant)"
    elif avg_g > avg_r and avg_g > avg_b and avg_g > 100:
        return "Banana (Green/Yellow dominant)"
    elif avg_r > 150 and avg_g > 100 and avg_g < 150:
        return "Orange"
    else:
        return "Unknown fruit"

# Fixed array creation - using uint8 type
red_test = np.full((100, 100, 3), [255, 0, 0], dtype=np.uint8)
green_test = np.full((100, 100, 3), [0, 255, 0], dtype=np.uint8)
blue_test = np.full((100, 100, 3), [0, 0, 255], dtype=np.uint8)
orange_test = np.full((100, 100, 3), [255, 165, 0], dtype=np.uint8)

red_img = Image.fromarray(red_test)
green_img = Image.fromarray(green_test)
blue_img = Image.fromarray(blue_test)
orange_img = Image.fromarray(orange_test)

print("Testing pure red image:")
result = detect_fruit_by_color(red_img)
print(f"Result: {result}\n")

print("Testing pure green image:")
result = detect_fruit_by_color(green_img)
print(f"Result: {result}\n")

print("Testing pure blue image:")
result = detect_fruit_by_color(blue_img)
print(f"Result: {result}\n")

print("Testing pure orange image:")
result = detect_fruit_by_color(orange_img)
print(f"Result: {result}\n")
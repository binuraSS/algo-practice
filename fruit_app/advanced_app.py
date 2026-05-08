import streamlit as st
from PIL import Image
import numpy as np

st.title("🍎 Advanced Fruit Detector")
st.write("With background elimination")

def get_fruit_color_advanced(img):
    """Ignore edges where background might be"""
    
    # Convert to numpy array
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Method 1: Take only the CENTER 50% of the image
    center_h_start = h // 4
    center_h_end = 3 * h // 4
    center_w_start = w // 4
    center_w_end = 3 * w // 4
    
    center_region = img_array[center_h_start:center_h_end, center_w_start:center_w_end]
    
    # Calculate average of center only
    avg_r = center_region[:,:,0].mean()
    avg_g = center_region[:,:,1].mean()
    avg_b = center_region[:,:,2].mean()
    
    # Method 2: Also check the whole image for comparison
    full_r = img_array[:,:,0].mean()
    full_g = img_array[:,:,1].mean()
    full_b = img_array[:,:,2].mean()
    
    return (avg_r, avg_g, avg_b), (full_r, full_g, full_b)

def grayscale_analysis(img):
    """Analyze using grayscale to detect shapes"""
    img_array = np.array(img.convert('L'))  # Convert to grayscale
    h, w = img_array.shape
    
    # Take center region
    center = img_array[h//4:3*h//4, w//4:3*w//4]
    
    # Calculate statistics
    mean_brightness = center.mean()
    std_brightness = center.std()
    min_brightness = center.min()
    max_brightness = center.max()
    
    return mean_brightness, std_brightness, min_brightness, max_brightness

def edge_detection_simple(img):
    """Simple edge detection to find fruit boundaries"""
    img_array = np.array(img.convert('L'))
    
    # Simple edge detection using difference between adjacent pixels
    h, w = img_array.shape
    edges = np.zeros_like(img_array)
    
    for i in range(1, h-1):
        for j in range(1, w-1):
            # Check difference with neighbors
            diff_x = abs(int(img_array[i, j+1]) - int(img_array[i, j-1]))
            diff_y = abs(int(img_array[i+1, j]) - int(img_array[i-1, j]))
            edges[i, j] = max(diff_x, diff_y)
    
    # Return average edge strength
    return edges.mean()

def advanced_predict(img):
    """Put it all together"""
    
    # Get colors from center only (background eliminated)
    (center_r, center_g, center_b), (full_r, full_g, full_b) = get_fruit_color_advanced(img)
    
    # Grayscale analysis
    mean_bright, std_bright, min_bright, max_bright = grayscale_analysis(img)
    
    # Edge detection
    edge_strength = edge_detection_simple(img)
    
    # Debug info
    st.caption(f"**Center colors:** 🟥{center_r:.0f} 🟩{center_g:.0f} 🟦{center_b:.0f}")
    st.caption(f"**Full image colors:** 🟥{full_r:.0f} 🟩{full_g:.0f} 🟦{full_b:.0f}")
    st.caption(f"**Edge strength:** {edge_strength:.1f} (higher = clearer edges)")
    
    # Color ratios from center (background eliminated)
    total = center_r + center_g + center_b
    if total == 0:
        return "Unknown", 0
    
    r_ratio = center_r / total
    g_ratio = center_g / total
    b_ratio = center_b / total
    
    st.caption(f"**Center ratios:** R:{r_ratio:.2f} G:{g_ratio:.2f} B:{b_ratio:.2f}")
    
    # Improved detection using center-only colors
    # Apple (Red) - high red ratio
    if r_ratio > 0.5 and center_r > 100:
        return "Apple (Red)", 90
    # Apple (Green) - high green ratio
    elif g_ratio > 0.4 and center_g > 80:
        return "Apple (Green)", 85
    # Banana - high green/yellow (R and G balanced)
    elif g_ratio > 0.35 and r_ratio > 0.3 and center_b < center_g:
        return "Banana", 80
    # Orange - medium red, medium green, low blue
    elif r_ratio > 0.4 and g_ratio > 0.25 and b_ratio < 0.25:
        return "Orange", 85
    # Lemon - high green and red, low blue
    elif g_ratio > 0.35 and r_ratio > 0.35 and b_ratio < 0.3:
        return "Lemon", 75
    else:
        return "Fruit", 50

# Remedy database
remedies = {
    'Apple (Red)': {'fresh': "Store in fridge for 2 weeks", 'bruised': "Eat within 2 days"},
    'Apple (Green)': {'fresh': "Store in fridge, great for pies", 'bruised': "Use in salads"},
    'Banana': {'fresh': "Room temperature", 'green': "Wait 3 days to ripen", 'overripe': "Make banana bread"},
    'Orange': {'fresh': "Store in fridge", 'hard': "Roll to soften", 'dry': "Use for zest"},
    'Lemon': {'fresh': "Fridge for 3 weeks", 'dry': "Soak in warm water", 'hard': "Roll before juicing"},
    'Fruit': {'fresh': "Store in cool, dry place"}
}

# UI
uploaded = st.file_uploader("Upload a fruit photo", type=['jpg', 'png', 'jpeg'])

if uploaded:
    img = Image.open(uploaded)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(img, width=250)
    
    with col2:
        fruit, confidence = advanced_predict(img)
        st.success(f"**Detected: {fruit}**")
        st.metric("Confidence", f"{confidence}%")
    
    # Show which part of image we're analyzing
    with st.expander("🔍 How detection works"):
        st.write("""
        **Background elimination methods:**
        1. **Center focus** - Only analyzes middle 50% of image
        2. **Edge detection** - Finds where fruit boundaries are
        3. **Grayscale analysis** - Measures brightness patterns
        """)
        
        # Show center region
        img_array = np.array(img)
        h, w = img_array.shape[:2]
        center_h_start = h // 4
        center_h_end = 3 * h // 4
        center_w_start = w // 4
        center_w_end = 3 * w // 4
        
        from PIL import ImageDraw
        img_with_box = img.copy()
        draw = ImageDraw.Draw(img_with_box)
        draw.rectangle([center_w_start, center_h_start, center_w_end, center_h_end], outline="red", width=3)
        st.image(img_with_box, caption="Analyzed center region (red box)", width=250)
    
    # Remedy section
    st.subheader("💡 Remedy")
    if fruit in remedies:
        condition = st.selectbox("Condition", list(remedies[fruit].keys()))
        st.success(remedies[fruit][condition])
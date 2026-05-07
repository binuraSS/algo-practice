import streamlit as st
from PIL import Image
import numpy as np

def detect_fruit_by_color(img):
    # Resize and convert to array
    img = img.resize((100, 100))
    img_array = np.array(img)
    
    # Get average RGB
    avg_r = img_array[:,:,0].mean()
    avg_g = img_array[:,:,1].mean()
    avg_b = img_array[:,:,2].mean()
    
    # Calculate ratios for better detection
    total = avg_r + avg_g + avg_b
    if total == 0:
        return "Unknown", 0
    
    r_ratio = avg_r / total
    g_ratio = avg_g / total
    b_ratio = avg_b / total
    
    # Display debug info (only when running, remove later)
    print(f"RGB: ({avg_r:.0f}, {avg_g:.0f}, {avg_b:.0f})")
    print(f"Ratios - R:{r_ratio:.2f}, G:{g_ratio:.2f}, B:{b_ratio:.2f}")
    
    # Better detection logic
    # Orange: High red, medium green, low blue (R>G>B)
    if avg_r > 150 and avg_g > 80 and avg_g < 150 and avg_b < 100:
        return "Orange", 85
    
    # Apple (Red): Very high red, low green and blue
    elif avg_r > 150 and avg_g < 100 and avg_b < 100:
        return "Apple", 90
    
    # Banana (Yellow/Green): High green, medium red, low blue
    elif avg_g > 120 and avg_r > 80 and avg_b < 100:
        return "Banana", 80
    
    # Lemon: High green and yellow (R and G balanced, low B)
    elif avg_g > 100 and avg_r > 100 and avg_b < 80:
        return "Lemon", 75
    
    else:
        return "Fruit", 50

st.title("🍎 Fruit Color Detector")
st.write("Upload a fruit photo - works best on solid backgrounds!")

uploaded = st.file_uploader("Choose image", type=['jpg','png','jpeg'])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, width=250)
    
    fruit, confidence = detect_fruit_by_color(img)
    
    st.success(f"**Detected: {fruit}** (Confidence: {confidence}%)")
    
    # Show the RGB values for transparency
    img_array = np.array(img.resize((100, 100)))
    avg_r = img_array[:,:,0].mean()
    avg_g = img_array[:,:,1].mean()
    avg_b = img_array[:,:,2].mean()
    st.caption(f"Average colors: 🟥 {avg_r:.0f} 🟩 {avg_g:.0f} 🟦 {avg_b:.0f}")
    
    remedies = {
        'Apple': {
            'fresh': "🍎 Store in refrigerator crisper drawer for up to 2 weeks",
            'bruised': "🍎 Eat within 2 days or make applesauce",
            'unripe': "🍎 Leave at room temperature for 3-5 days"
        },
        'Banana': {
            'fresh': "🍌 Store at room temperature away from sunlight",
            'green': "🍌 Leave at room temperature for 3 days until yellow",
            'overripe': "🍌 Perfect for banana bread! Freeze for later"
        },
        'Orange': {
            'fresh': "🍊 Store in refrigerator for up to 2 weeks",
            'hard': "🍊 Roll on counter to soften before eating",
            'dry': "🍊 Use for zest or marmalade"
        },
        'Lemon': {
            'fresh': "🍋 Store in refrigerator for up to 3 weeks",
            'dry': "🍋 Soak in warm water for 10 minutes before juicing",
            'hard': "🍋 Roll on counter to release more juice"
        },
        'Fruit': {
            'fresh': "Store in cool, dry place away from sunlight"
        }
    }
    
       # Let user choose condition
    if fruit in remedies:
        conditions = list(remedies[fruit].keys())
        condition = st.selectbox("What condition is your fruit in?", conditions)
        st.info(f"💡 **Remedy:** {remedies[fruit][condition]}")
    else:
        st.info(f"💡 **Remedy:** {remedies['Fruit']['fresh']}")
    
    st.warning("📝 **Tip:** For best results, use photos with plain backgrounds and good lighting!")
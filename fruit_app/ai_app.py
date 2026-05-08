import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

st.set_page_config(page_title="AI Fruit Classifier", page_icon="🍎")

st.title("🍎 AI-Powered Fruit Classifier")
st.write("Using Neural Networks + Color Detection")

# Try to load the AI model
@st.cache_resource
def load_ai_model():
    try:
        if os.path.exists('fruit_classifier.keras'):
            model = load_model('fruit_classifier.keras')
            return model, True
        else:
            st.warning("AI model not found. Using color detection only.")
            return None, False
    except Exception as e:
        st.warning(f"Could not load AI model: {e}")
        return None, False

model, has_ai = load_ai_model()

# Fruit names (must match training order)
ai_fruit_names = ['Apple', 'Banana', 'Lemon', 'Orange']

def ai_predict(img):
    """Use trained neural network"""
    if not has_ai:
        return None, 0
    
    # Prepare image for AI
    img = img.resize((100, 100))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    prediction = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(prediction[0])
    confidence = np.max(prediction[0]) * 100
    
    return ai_fruit_names[predicted_class], confidence

def color_predict(img):
    """Fallback color detection"""
    img = img.resize((100, 100))
    img_array = np.array(img)
    
    avg_r = img_array[:,:,0].mean()
    avg_g = img_array[:,:,1].mean()
    avg_b = img_array[:,:,2].mean()
    
    # Orange detection
    if avg_r > 150 and avg_g > 80 and avg_g < 150 and avg_b < 100:
        return "Orange", 75
    # Red Apple
    elif avg_r > 150 and avg_g < 100 and avg_b < 100:
        return "Apple", 80
    # Banana
    elif avg_g > 120 and avg_r > 80 and avg_b < 100:
        return "Banana", 70
    # Lemon
    elif avg_g > 100 and avg_r > 100 and avg_b < 80:
        return "Lemon", 65
    else:
        return "Unknown", 40

# Remedies database
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
    'Unknown': {
        'fresh': "Store in cool, dry place away from sunlight"
    }
}

# Upload section
uploaded = st.file_uploader("📸 Upload a fruit photo", type=['jpg', 'jpeg', 'png'])

if uploaded:
    # Display image
    img = Image.open(uploaded)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(img, width=250, caption="Your fruit")
    
    # Get predictions
    ai_fruit, ai_conf = ai_predict(img)
    color_fruit, color_conf = color_predict(img)
    
    # Show results
    with col2:
        st.subheader("🔍 Results")
        
        if has_ai and ai_conf > 60:
            st.success(f"**AI Neural Network**")
            st.write(f"🍎 {ai_fruit}")
            st.write(f"Confidence: {ai_conf:.1f}%")
            final_fruit = ai_fruit
        else:
            st.info(f"**Color Detection** (AI unavailable/low confidence)")
            st.write(f"🍎 {color_fruit}")
            st.write(f"Confidence: {color_conf:.1f}%")
            final_fruit = color_fruit
    
    # Condition selector
    st.divider()
    st.subheader("📋 Select fruit condition")
    
    if final_fruit in remedies:
        condition = st.selectbox("What condition is your fruit in?", 
                                  list(remedies[final_fruit].keys()))
        
        st.subheader("💡 Recommended Remedy")
        st.success(remedies[final_fruit][condition])
    else:
        st.info(remedies['Unknown']['fresh'])
    
    # Show debug info
    with st.expander("🔧 Technical Details"):
        if has_ai:
            st.write(f"AI Model: Loaded successfully")
            st.write(f"AI Confidence: {ai_conf:.1f}%")
        st.write(f"Color Detection Confidence: {color_conf:.1f}%")
        st.write(f"Final prediction: {final_fruit}")

else:
    st.info("👈 Upload a fruit photo to get started!")
    
    # Show example
    with st.expander("📖 How to get best results"):
        st.write("""
        1. Use clear photos with good lighting
        2. Place fruit on a plain background
        3. Make sure the fruit is centered
        4. Avoid shadows on the fruit
        """)

st.divider()
st.caption("Built with TensorFlow + Streamlit | Trained on Fruits-360 dataset")
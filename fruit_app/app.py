import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the working model
model = load_model('fruit_model.h5')

# Fruit names
fruit_names = ['Apple', 'Banana', 'Lemon', 'Orange', 'Mango', 'Strawberry']

# Remedies
remedies = {
    'Apple': {'fresh': 'Store in fridge for 2 weeks', 'bruised': 'Eat within 2 days'},
    'Banana': {'fresh': 'Room temperature', 'green': 'Wait 3 days to ripen'},
    'Lemon': {'fresh': 'Fridge for 3 weeks', 'dry': 'Soak in warm water'},
    'Orange': {'fresh': 'Fridge for 2 weeks', 'hard': 'Roll to soften'},
    'Mango': {'fresh': 'Room temperature', 'unripe': 'Keep in paper bag'},
    'Strawberry': {'fresh': 'Fridge, eat within 3 days', 'moldy': 'Discard immediately'}
}

st.title("🍎 Fruit Classifier")
st.write("Upload a fruit photo")

uploaded = st.file_uploader("Choose an image", type=['jpg','png','jpeg'])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, width=300)
    
    # Prepare image
    img = img.resize((100,100))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    pred = model.predict(img_array)
    fruit = fruit_names[np.argmax(pred[0])]
    confidence = np.max(pred[0]) * 100
    
    st.success(f"**Prediction: {fruit}** ({confidence:.1f}%)")
    
    condition = st.selectbox("Condition", list(remedies[fruit].keys()))
    st.info(f"**Remedy:** {remedies[fruit][condition]}")
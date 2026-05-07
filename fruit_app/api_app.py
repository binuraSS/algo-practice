import streamlit as st
from PIL import Image
import requests
import json

st.title("🍎 Fruit Helper")
st.write("Upload any fruit photo")

uploaded = st.file_uploader("Choose image", type=['jpg','png','jpeg'])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, width=250)
    
    # Let user select fruit manually (practical solution)
    fruit = st.selectbox("What fruit is this?", 
                         ["Apple", "Banana", "Orange", "Lemon", "Mango", "Strawberry"])
    
    condition = st.selectbox("Condition", 
                             ["Fresh", "Bruised", "Unripe", "Overripe"])
    
    remedies = {
        "Apple": {"Fresh": "Store in fridge for 2 weeks", 
                  "Bruised": "Eat within 2 days", 
                  "Unripe": "Leave at room temperature"},
        "Banana": {"Fresh": "Room temperature", 
                   "Bruised": "Eat today or freeze", 
                   "Overripe": "Make banana bread!"},
        "Orange": {"Fresh": "Store in fridge", 
                   "Hard": "Roll on counter to soften", 
                   "Dry": "Use for zest"},
        "Lemon": {"Fresh": "Fridge for 3 weeks", 
                  "Dry": "Soak in warm water", 
                  "Hard": "Roll before juicing"}
    }
    
    st.success(f"**Selected: {fruit}**")
    st.info(f"💡 **Remedy:** {remedies.get(fruit, {}).get(condition, 'Store normally')}")
    
    st.caption("Note: AI fruit detection is complex. This app lets you select the fruit manually.")
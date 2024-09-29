import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Streamlit app title and description
st.title("Image Classification with Keras Model")
st.write("Upload an image to classify it using a pre-trained Keras model.")

@st.cache_resource
def load_my_model():
    """Load the Keras model and labels (cached to avoid reloading)."""
    model = load_model("keras_Model.h5", compile=False)
    class_names = open("labels.txt", "r").readlines()
    return model, class_names

model, class_names = load_my_model()

# File uploader for uploading images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Open and display the uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Preprocess the image: resize and normalize
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)

        # Normalize the image array
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Create a batch of size 1 (1, 224, 224, 3)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # Add a progress bar or loading message
        with st.spinner('Classifying image...'):
            # Make the prediction
            prediction = model.predict(data)
        
        # Get top 3 predictions and confidence scores
        top_indices = np.argsort(prediction[0])[-3:][::-1]
        st.write("### Predictions")
        for i in top_indices:
            class_name = class_names[i]
            confidence_score = prediction[0][i]
            st.write(f"*Class:* {class_name[2:].strip()} | *Confidence Score:* {confidence_score:.2f}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.write("Please upload an image to classify.")

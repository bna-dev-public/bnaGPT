from PIL import Image
import streamlit as st


@st.cache_data(ttl=300)
def load_image(filename: str) -> Image.Image:
    return Image.open(filename)

import streamlit as st
from PIL import Image, UnidentifiedImageError
import pyheif
import io

def convert_heic_to_jpg(input_bytes):
    try:
        heif_file = pyheif.read(input_bytes)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    except pyheif.error.HeifError as e:
        st.error(f"Error reading HEIC file: {e}")
        return None
    except UnidentifiedImageError as e:
        st.error(f"Cannot identify image file: {e}")
        return None
    output_bytes = io.BytesIO()
    image.save(output_bytes, "JPEG")
    output_bytes.seek(0)
    return output_bytes

st.title("HEIC to JPG Converter")

uploaded_file = st.file_uploader("Choose a HEIC file", type="heic")

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded HEIC image', use_container_width=True)
    st.write("\nConverting...")

    output_bytes = convert_heic_to_jpg(uploaded_file.read())

    st.image(output_bytes, caption='Converted JPG image', use_container_width=True)
    st.download_button(
        label="Download JPG",
        data=output_bytes,
        file_name="converted_image.jpg",
        mime="image/jpeg"
    )

    st.write("\nDone!")

else:
    st.write("Please upload a HEIC file.")
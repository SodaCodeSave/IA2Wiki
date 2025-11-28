import streamlit as st
import func
import os

st.title("IA2Wiki")
st.text("Automatically identify ItemsAdder files and generate item documentation.")
items_adder_path = st.text_input("Please enter the location of the Items Adder file")
if st.button("Start"):
    if os.path.exists(items_adder_path):
        print("Starting")
        result = func.scan_yml_files(items_adder_path)
        missing_images = list(result[1])  # Convert missing image filenames set to list
        item_names = list(result[2])  # Convert item names set to list
        missing_images_text = ""
        from itertools import zip_longest
        for missing_image, display_name in zip_longest(missing_images, item_names, fillvalue="Unknown or Minecraft Item"):
            missing_images_text += f"{missing_image.split(":")[-1].lower()} ({display_name})\n\n"
        st.success("All done, please check wiki directory!")
        st.warning(f"You need these images, please place them in the static folder in the same directory as the document: \n{missing_images_text}")
    else:
        st.error("Please enter a valid location")
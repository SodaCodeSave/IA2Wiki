import streamlit as st
import func
import os

st.title("IA2Wiki")
st.text("Automatically identify Items Adder files and write item documents")
loc = st.text_input("Please enter the location of the Items Adder file")
if st.button("Start"):
    if os.path.exists(loc):
        print("Starting")
        r = func.scan_yml_files(loc)
        items = list(r[1])  # 缺失的图片文件名集合转为列表
        item_names = list(r[2])  # 物品名称集合转为列表
        item = ""
        for i in range(len(items)):
            # 修复索引访问，确保使用正确的索引
            item_name = item_names[i] if i < len(item_names) else "Unknown or Minecraft Item"
            item += f"{items[i].split(":")[-1].lower()} ({item_name})\n\n"
        st.success("All done")
        st.warning(f"You need these images, please place them in the static folder in the same directory as the document: \n{item}")
    else:
        st.error("Please enter a valid location")
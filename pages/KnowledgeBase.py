import os

import pandas as pd
import streamlit as st
from utils.db import chroma_source
st.set_page_config(page_title='Qwen-Chatbot')  # 页面标题
st.header('knowledge_base :robot_face:')  # 标题头
st.sidebar.markdown("## Config")

name = st.text_area(
        label="知识库名字",
    )

file_content = st.text_area(
    label="知识库的描述"
)
folder_path = "knowledge_base/"+name
# 创建文件夹
# 获取用户输入的文件内容

# 添加按钮用于创建文件夹并保存文件内容
if st.button("创建知识库文件夹"):
    # 检查文件夹路径和文件内容是否都不为空
    if folder_path.strip() and file_content.strip():
        # 使用os.makedirs()函数创建文件夹
        os.makedirs(folder_path, exist_ok=True)
        # 构造文件路径
        file_path = os.path.join(folder_path, "file.txt")
        # 将用户输入的文件内容写入文件中
        with open(file_path, "w") as f:
            f.write(file_content)
        st.success(f"File saved successfully at '{file_path}'.")
    else:
        st.error("Please enter both folder path and file content.")


# 显示现有知识库
base_name = os.listdir("knowledge_base")
d_base = []
for name in base_name:
    d_base.append(name)

data_base = pd.DataFrame({
    '知识库': d_base,
})

data_base_name = st.selectbox("已有知识库",data_base['知识库'])
base_path = "knowledge_base/"+data_base_name
# 上传文件
uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
save_path = "knowledge_base/"+data_base_name+"/knowledge"
if not os.path.exists(save_path):
    os.makedirs(save_path, exist_ok=True)
if uploaded_files:

    for uploaded_file in uploaded_files:
        filename = os.path.join(save_path, uploaded_file.name)
        with open(filename, "wb") as f:
            f.write(uploaded_file.getvalue())

    chroma_source(base_path)
    st.success(f"Files saved successfully at '{save_path}'. and create KnowledgeBase")


# 删除
import shutil


# 添加一个按钮用于删除文件
if st.button("Delete file"):
    # 检查文件是否存在，如果存在则删除
    if os.path.exists(base_path):
        # 删除目录及其内容
        shutil.rmtree(base_path)
        st.success("File deleted successfully.")
    else:
        st.error("File does not exist.")
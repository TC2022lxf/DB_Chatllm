import streamlit as st

st.markdown("# Qwen 🎉")
st.sidebar.markdown("# 流式输出，纯llm无上下文知识库，结果无保留 🎉")

import pandas as pd
import streamlit as st
import torch
from langchain_community.chat_models import ChatOllama
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage, HumanMessage
from utils.retriever import retrievers
from utils.load_data import load_data
from utils.llm import *

llm = ChatOllama(base_url="http://localhost:11434",
                 model=st.session_state.llm,
                 callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

if 'messages1' not in st.session_state:  # 检查 st.session_state 中是否存在名为 'messages' 的键
    st.session_state['messages1'] = []
messages = st.session_state.get('messages1', [])  # 获取messages
print(messages)
for message in messages:  # 遍历每一条信息
    if isinstance(message, AIMessage):  # 检查变量 message 是否是一个名为 AIMessage 的类的实例。
        with st.chat_message('assistant'):  # 创建一个聊天消息框，
            st.markdown(message.content)  # 消息内容以 Markdown 格式显示。
    elif isinstance(message, HumanMessage):
        with st.chat_message('user'):  # 创建一个user的聊天消息框，
            st.markdown(message.content)

if user_input := st.chat_input("Enter your question here"):  # chat_input创建聊天输入框->user_input
    st.session_state.messages1.append(HumanMessage(content=user_input))  # 输入内容作为一个HM对象实例被添加到st.session_state.messages列表中
    st.chat_message("user").markdown(user_input)  # 显示用户刚刚输入的问题，标记为用户消息
    with st.chat_message("assistant"):  # 下面的代码生成llm的回答->assistant
        response = llm.stream(input=user_input)
        st.write_stream(response)
    st.session_state.messages1.append(AIMessage(content=response))

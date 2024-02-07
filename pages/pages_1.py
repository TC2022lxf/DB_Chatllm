import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

st.markdown("# chat_prompt_no_history 🎉")
st.sidebar.markdown("# Page 1 🎉")
st.sidebar.markdown("## 没有历史记录、每次回答会显示来源但不保存")

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
docsearch = chroma_source().as_retriever()
if 'messages2' not in st.session_state:  # 检查 st.session_state 中是否存在名为 'messages' 的键
    st.session_state['messages2'] = []
messages = st.session_state.get('messages2', [])  # 获取messages
print(messages)
for message in messages:  # 遍历每一条信息
    if isinstance(message, AIMessage):  # 检查变量 message 是否是一个名为 AIMessage 的类的实例。
        with st.chat_message('assistant'):  # 创建一个聊天消息框，
            st.markdown(message.content)  # 消息内容以 Markdown 格式显示。
    elif isinstance(message, HumanMessage):
        with st.chat_message('user'):  # 创建一个user的聊天消息框，
            st.markdown(message.content)

if user_input := st.chat_input("Enter your question here"):  # chat_input创建聊天输入框->user_input
    st.session_state.messages2.append(HumanMessage(content=user_input))  # 输入内容作为一个HM对象实例被添加到st.session_state.messages列表中
    st.chat_message("user").markdown(user_input)  # 显示用户刚刚输入的问题，标记为用户消息
    with st.chat_message("assistant"):  # 下面的代码生成llm的回答->assistant
        chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt1())
        docs = docsearch.get_relevant_documents(user_input)
        result=chain({"input_documents": docs, "question": user_input}, return_only_outputs=True)
        st.markdown("## 答案来源：")
        st.markdown(docs)
        st.markdown("## 答案：")
        st.markdown(result["output_text"])
    st.session_state.messages2.append(AIMessage(content=result["output_text"]))
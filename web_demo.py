# 左侧超参数调节组件
# st表示streamlit
import pandas as pd
import streamlit as st
import torch
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage, HumanMessage
from utils.retriever import retrievers
from utils.load_data import load_data
from utils.llm import *

st.set_page_config(page_title='Qwen-Chatbot')  # 页面标题
st.header('Chat_config:robot_face:')  # 标题头

# 设置max_length、top_p和temperature，在侧边栏设置滑动条
if "max_length" not in st.session_state:
    st.session_state["max_length"] = 2024
    st.sidebar.slider("max_length", 0, 32768, st.session_state["max_length"], step=1)
else:
    st.session_state["max_length"] = st.sidebar.slider("max_length", 0, 32768, st.session_state["max_length"], step=1)

# 设置top_p
if "top_p" not in st.session_state:
    st.session_state["top_p"] = 0.8
    st.sidebar.slider("top_p", 0.0, 1.0, st.session_state["top_p"], step=0.01)
else:
    st.session_state["top_p"] = st.sidebar.slider("top_p", 0.0, 1.0, st.session_state["top_p"], step=0.01)

# 设置temperature
if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.6
    st.sidebar.slider("temperature", 0.0, 1.0, st.session_state["temperature"], step=0.01)
else:
    st.session_state["temperature"] = st.sidebar.slider("temperature", 0.0, 1.0, st.session_state["temperature"],
                                                        step=0.01)

data_base = pd.DataFrame({
    '知识库': [1, 2, 3, 4],
})
llm_option = pd.DataFrame({
    '语言模型': ["qwen", "qwen-7B"]
})

# 选择知识库
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = st.sidebar.selectbox(
        '知识库的选择',
        data_base['知识库'])
else:
    st.session_state.knowledge_base = st.sidebar.selectbox(
        '知识库的选择',
        data_base['知识库'],
        index=data_base.index[data_base['知识库'] == st.session_state.knowledge_base].tolist()[0]
    )

# 选择模型
if "llm" not in st.session_state:
    st.session_state.llm = st.sidebar.selectbox(
        '语言模型的选择',
        llm_option['语言模型'])
else:
    st.session_state.llm = st.sidebar.selectbox(
        '语言模型的选择',
        llm_option['语言模型'],
        index=llm_option.index[llm_option['语言模型'] == st.session_state.llm].tolist()[0]
    )

# 设置prompt1，有聊天历史和问题
import streamlit as st
from langchain_core.prompts import PromptTemplate

if "CONDENSE_QUESTION_PROMPT" not in st.session_state:

    st.session_state.CONDENSE_QUESTION_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""
    st.session_state.CONDENSE_QUESTION_PROMPT = st.text_area(
        "prompt_template(history,question)",
        st.session_state.CONDENSE_QUESTION_PROMPT,
        300,
        max_chars=5000,
    )

else:
    st.session_state.CONDENSE_QUESTION_PROMPT = st.text_area(
        "prompt_template(history,question)",
        st.session_state.CONDENSE_QUESTION_PROMPT,
        300,
        max_chars=5000,
    )
# 设置提示词二，有上下文和问题
if "QA_PROMPT" not in st.session_state:

    st.session_state.QA_PROMPT = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Helpful Answer:"""
    st.session_state.QA_PROMPT = st.text_area(
        "prompt2_template(context,question)",
        st.session_state.QA_PROMPT,
        300,
        max_chars=5000,
    )

else:
    st.session_state.QA_PROMPT = st.text_area(
        "prompt2_template(context,question)",
        st.session_state.QA_PROMPT,
        300,
        max_chars=5000,
    )



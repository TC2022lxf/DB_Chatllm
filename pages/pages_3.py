import threading

import pandas as pd
import streamlit as st
import torch
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import LLMResult

from utils.retriever import retrievers
from utils.load_data import load_data
from utils.llm import *

st.set_page_config(page_title='Qwen-Chatbot')  # 页面标题
st.header('Qwen-Powered Chatbot :robot_face:')  # 标题头
st.sidebar.markdown("## 测试，无流式输出")

# 设置max_length、top_p和temperature，在侧边栏设置滑动条
# 加载模型
llm = Ollama(base_url="http://localhost:11434",
             model=st.session_state.llm,
             callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
             top_p=st.session_state.top_p, temperature=st.session_state.temperature
             )
print(st.session_state.llm)

# 加载数据库
persist_directory = os.path.join('knowledge_base', st.session_state["knowledge_base"])
print(persist_directory)
# embedding model
model = embedding_data()
if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:  # 检查目录是否为空
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
else:
    st.error('数据库错误,可能没有加载成功')

# 加载提示词
CONDENSE_QUESTION_PROMPT = PromptTemplate(
    template=st.session_state.CONDENSE_QUESTION_PROMPT, input_variables=["question"]
)
QA_PROMPT = PromptTemplate(
    template=st.session_state.QA_PROMPT, input_variables=["context", "chat_history","question"]
)

# 清理会话历史按钮
buttonClean = st.sidebar.button("清理会话历史", key="clean")  # 侧边栏中定义了一个按钮，该按钮的文本标签是“清理会话历史” key用于区分多个按钮，
if buttonClean:  # 如果被点击了
    st.session_state.history3 = []  # history 清空
    # st.session_state['messages1'] = []
    st.session_state.past_key_values = None  # 表示清除之前保存的某项关键信息或历史状态。
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # 清空 CUDA 显存中的缓存。
    st.rerun()  # 调用此方法将重新运行应用程序

# 聊天记录
if 'chat_history3' not in st.session_state:
    st.session_state['chat_history3'] =[]
# 打印历史信息
if 'history3' not in st.session_state:  # 检查 st.session_state 中是否存在名为 'messages' 的键
    st.session_state['history3'] = []
messages = st.session_state.get('history3', [])  # 获取messages

for message in messages:  # 遍历每一条信息
    if isinstance(message, AIMessage):  # 检查变量 message 是否是一个名为 AIMessage 的类的实例。
        with st.chat_message('assistant'):  # 创建一个聊天消息框，
            st.markdown(message.content)  # 消息内容以 Markdown 格式显示。
    elif isinstance(message, HumanMessage):
        with st.chat_message('user'):  # 创建一个user的聊天消息框，
            st.markdown(message.content)

# 输入问题并回答
if user_input := st.chat_input("Enter your question here"):  # chat_input创建聊天输入框->user_input
    st.session_state.history.append(HumanMessage(content=user_input))  # 输入内容作为一个HM对象实例被添加到st.session_state.messages3列表中
    st.chat_message("user").markdown(user_input)  # 显示用户刚刚输入的问题，标记为用户消息
    with st.chat_message("assistant"):  # 下面的代码生成llm的回答->assistant
        question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_PROMPT)
        qa = ConversationalRetrievalChain(
            retriever=vectorstore.as_retriever(), combine_docs_chain=chain, question_generator=question_generator,
            return_source_documents=True)
        result = qa({"question": user_input, "chat_history": st.session_state.chat_history3}, return_only_outputs=True)
        st.markdown("## 答案来源：")
        st.markdown(result["source_documents"])
        st.markdown("## 答案：")
        st.markdown(result["answer"])
    st.session_state.history.append(AIMessage(content=result["answer"]))
    st.session_state['chat_history'].append((user_input,result["answer"]))

import time

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate

st.markdown("# test 2 🎉")
st.sidebar.markdown("# Page 2 🎉")
st.sidebar.markdown("## 不返回答案来源")

from langchain.llms.base import LLM
import pandas as pd
import streamlit as st
import torch
from langchain_community.chat_models import ChatOllama
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage, HumanMessage
from utils.retriever import retrievers
from utils.load_data import load_data
from utils.llm import *

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.str = ''
        # 记得结束后这里置true
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        print(token)
        self.str +=token
        self.tokens.append(token)

    def on_llm_end(self, response: LLMResult, **kwargs: any) -> None:
        self.finish = 1

    def on_llm_error(self, error: Exception, **kwargs: any) -> None:
        print(str(error))
        self.tokens.append(str(error))

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                pass


chainStreamHandler = ChainStreamHandler()
llm = ChatOllama(base_url="http://localhost:11434",
                 model=st.session_state.llm,
                 callback_manager=CallbackManager([chainStreamHandler]))

llm1 = ChatOllama(base_url="http://localhost:11434",
                 model="qwen:14b",
                 callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# 加载提示词
CONDENSE_QUESTION_PROMPT = PromptTemplate(
    template=st.session_state.CONDENSE_QUESTION_PROMPT, input_variables=["question"]
)
QA_PROMPT = PromptTemplate(
    template=st.session_state.QA_PROMPT, input_variables=["context", "chat_history","question"]
)


# 加载数据库
persist_directory = os.path.join('knowledge_base', st.session_state["knowledge_base"])
print(persist_directory)
# embedding model
model = embedding_data()
if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:  # 检查目录是否为空
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
else:
    st.error('数据库错误,可能没有加载成功')

if 'chat_history1' not in st.session_state:
    st.session_state['chat_history1'] =[]
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

import threading

def async_thread(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()


if user_input := st.chat_input("Enter your question here"):  # chat_input创建聊天输入框->user_input
    st.session_state.messages2.append(HumanMessage(content=user_input))  # 输入内容作为一个HM对象实例被添加到st.session_state.messages列表中
    st.chat_message("user").markdown(user_input)  # 显示用户刚刚输入的问题，标记为用户消息
    with st.chat_message("assistant"):  # 下面的代码生成llm的回答->assistant
        question_generator = LLMChain(llm=llm1, prompt=CONDENSE_QUESTION_PROMPT)
        chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_PROMPT)
        qa = ConversationalRetrievalChain(
            retriever=vectorstore.as_retriever(), combine_docs_chain=chain, question_generator=question_generator,
            return_source_documents=True)
        async_thread(qa,{"question": user_input, "chat_history": st.session_state.chat_history1}, return_only_outputs=True)
        st.write_stream(chainStreamHandler.generate_tokens())
    st.session_state.messages2.append(AIMessage(content=chainStreamHandler.str))
    st.session_state['chat_history1'].append((user_input, chainStreamHandler.str))

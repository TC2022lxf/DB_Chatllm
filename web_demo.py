# 左侧超参数调节组件
# st表示streamlit
import streamlit as st
import torch
from langchain_core.messages import AIMessage, HumanMessage
from utils.retriever import retrievers
from utils.load_data import load_data
from utils.llm import *


st.set_page_config(page_title='Qwen-Chatbot')  # 页面标题
st.header('Qwen-Powered Chatbot :robot_face:')  # 标题头

# 设置max_length、top_p和temperature，在侧边栏设置滑动条
max_length = st.sidebar.slider("max_length", 0, 32768, 8192, step=1)  # sidebar是侧边栏 slider是滑动条 0是最小值 32768是最大值 8192是初始值
top_p = st.sidebar.slider("top_p", 0.0, 1.0, 0.8, step=0.01)
temperature = st.sidebar.slider("temperature", 0.0, 1.0, 0.6, step=0.01)

# st.session_state 是 Streamlit 提供的一个内置对象，用于在应用的整个生命周期内持久保存状态信息
# 初始化history
st.session_state.history = []
# 清理会话历史按钮
buttonClean = st.sidebar.button("清理会话历史", key="clean")  # 侧边栏中定义了一个按钮，该按钮的文本标签是“清理会话历史” key用于区分多个按钮，
if buttonClean:  # 如果被点击了
    st.session_state.history = []  # history 清空
    st.session_state.past_key_values = None  # 表示清除之前保存的某项关键信息或历史状态。
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # 清空 CUDA 显存中的缓存。
    st.rerun()  # 调用此方法将重新运行应用程序


if 'messages' not in st.session_state:  # 检查 st.session_state 中是否存在名为 'messages' 的键
    st.session_state['messages'] = []
messages = st.session_state.get('messages', [])  # 获取messages
print(messages)
for message in messages:  # 遍历每一条信息
    if isinstance(message, AIMessage):  # 检查变量 message 是否是一个名为 AIMessage 的类的实例。
        with st.chat_message('assistant'):  # 创建一个聊天消息框，
            st.markdown(message.content)  # 消息内容以 Markdown 格式显示。
    elif isinstance(message, HumanMessage):
        with st.chat_message('user'):  # 创建一个user的聊天消息框，
            st.markdown(message.content)

if user_input := st.chat_input("Enter your question here"):  # chat_input创建聊天输入框->user_input
    st.session_state.messages.append(HumanMessage(content=user_input))  # 输入内容作为一个HM对象实例被添加到st.session_state.messages列表中
    st.chat_message("user").markdown(user_input)  # 显示用户刚刚输入的问题，标记为用户消息
    with st.chat_message("assistant"):  # 下面的代码生成llm的回答->assistant
        #similar_docs = retrievers(user_input)  # 根据回答检索出的知识文本 所以类似的文本都结合起来
        # context = "\n".join([document.page_content for document in similar_docs])
        #context = str(similar_docs[0].page_content)
        context = llm_no_prompt(user_input)
        # query_llm = LLMChain(llm=llm, prompt=prompt)  # , memory=memory)
        # response = query_llm.run({"context": context, "question": user_input})
        # response = response.replace("$", "\$")  # 字符串中所有的 $ 符号，并将其替换为 \$
        st.markdown(context)
    st.session_state.messages.append(AIMessage(content=context))

# new_answer = llm_chain.run(
#     context=context,
#     question=question,
#     max_length=max_length,
#     top_p=top_p,
#     temperature=temperature
# )

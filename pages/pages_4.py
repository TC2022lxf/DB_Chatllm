import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

st.markdown("# chat_source_answer 🎉")
st.sidebar.markdown("## 输出page 2 答案来源 🎉")

if 'messages' not in st.session_state:  # 检查 st.session_state 中是否存在名为 'messages' 的键
    st.session_state['messages'] = []
messages = st.session_state.get('messages', [])  # 获取messages

for message in messages:  # 遍历每一条信息
    if isinstance(message, AIMessage):  # 检查变量 message 是否是一个名为 AIMessage 的类的实例。
        with st.chat_message('assistant'):  # 创建一个聊天消息框，
            st.markdown(message.content)  # 消息内容以 Markdown 格式显示。
    elif isinstance(message, HumanMessage):
        with st.chat_message('user'):  # 创建一个user的聊天消息框，
            st.markdown(message.content)

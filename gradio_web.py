import os

import gradio as gr
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import PromptTemplate

from utils.embedding_data import embedding_data
from utils.llm import load_llm
llm = load_llm()
QA_PROMPT="""使用以下上下文和聊天历史记录来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案.

    上下文: {context}
    
    聊天历史记录: {chat_history}
    
    问题: {question}
    有帮助的答案:"""
QA_PROMPT = PromptTemplate(
    template=QA_PROMPT, input_variables=["context", "chat_history","question"]
)
# 加载数据库
persist_directory = os.path.join('knowledge_base', "chroma")
print(persist_directory)
# embedding model
model = embedding_data()
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
def echo(message, history):
    chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_PROMPT)
    docs = vectorstore.as_retriever().get_relevant_documents(message)
    result = chain({"input_documents": docs, "question": message, "chat_history": history}, return_only_outputs=True)
    print(message,history)
    print(type(result['output_text']))
    print(type(message))
    return result['output_text']

demo = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")
demo.launch(share=True)
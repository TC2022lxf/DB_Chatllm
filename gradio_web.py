# import os
#
# import gradio as gr
# from langchain.chains.question_answering import load_qa_chain
# from langchain_community.vectorstores.chroma import Chroma
# from langchain_core.prompts import PromptTemplate
#
# from utils.embedding_data import embedding_data
# from utils.llm import load_llm
# llm = load_llm()
# QA_PROMPT="""使用以下上下文和聊天历史记录来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案.
#
#     上下文: {context}
#
#     聊天历史记录: {chat_history}
#
#     问题: {question}
#     有帮助的答案:"""
# QA_PROMPT = PromptTemplate(
#     template=QA_PROMPT, input_variables=["context", "chat_history","question"]
# )
# # 加载数据库
# persist_directory = os.path.join('knowledge_base', "chroma")
# print(persist_directory)
# # embedding model
# model = embedding_data()
# vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
# def echo(message, history):
#     chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_PROMPT)
#     docs = vectorstore.as_retriever().get_relevant_documents(message)
#     result = chain({"input_documents": docs, "question": message, "chat_history": history}, return_only_outputs=True)
#     print(message,history)
#     print(type(result['output_text']))
#     print(type(message))
#     return result['output_text']
#
# demo = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")
# demo.launch(share=True)

import requests
from bs4 import BeautifulSoup
import os
import urllib.request


def download_pdf_links_from_page(url, output_dir):
    # 1. 获取网页内容
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，这里会抛出异常
    html_content = response.text

    # 2. 解析HTML以找到PDF链接
    soup = BeautifulSoup(html_content, 'html.parser')
    pdf_links = soup.find_all('a', href=True, text=True)
    pdf_links = [link['href'] for link in pdf_links if link['href'].endswith('.pdf')]

    # 3. 下载PDF文件
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, link in enumerate(pdf_links):
        # 构建完整的URL（如果链接是相对路径的话）
        if not link.startswith('http'):
            link = f"{url}{link}"

            # 获取文件名（从URL的最后一个部分）
        filename = os.path.basename(urllib.parse.urlparse(link).path)
        output_path = os.path.join(output_dir, filename)

        # 下载文件
        with requests.get(link, stream=True) as r:
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {output_path}")

    # 使用函数


url = '你的网页URL'  # 替换为你要爬取的网页URL
output_dir = '下载的PDF存放目录'  # 替换为你希望存放PDF的目录路径
download_pdf_links_from_page(url, output_dir)
import os

from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_community.vectorstores.chroma import Chroma
from utils.embedding_data import embedding_data
from utils.load_data import *
from config import DEFAULT_KNOWLEDGE_BASE
def list_md_files(path):
    md_files=[file for file in os.listdir(path) if file.endswith('.md')]
    return md_files

def save_to_txt(file_list, output_file):
    with open(output_file, 'w') as f:
        for file_name in file_list:
            f.write(file_name + '\n')

def init_chroma(persist_directory):
    model = embedding_data()
    all_splits = ["我是人工智能也是护肤专家，你可以向我提问关于护肤的任何问题"]
    all_metadata = [{"Header 1": "你是谁", "Source": "introduce"}]
    vectorstore = Chroma.from_texts(texts=all_splits, metadatas=all_metadata, embedding=model,
                                    persist_directory=persist_directory)  # 标题和内容同时加载
    vectorstore.persist()

def chroma_source(persist_directory):
    '''
    路径下保证有knowledge文件夹，history.txt文件
    将路径下的knowledge文件内的md数据加载入知识库
    history记录加载过的文件，避免重复加载
    :return:
    '''
    # embedding model
    model = embedding_data()
    output_file = persist_directory + "/history.txt"
    knowledge_file = persist_directory + "/knowledge"
    if not os.path.exists(knowledge_file):
        os.makedirs(knowledge_file, exist_ok=True)
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:  # 知识库非空
        print("Chroma数据库已存在，无需重复创建.")
        # 读取已经记录过的文件
        with open(output_file, 'r') as f:
            existing_files = set(f.read().splitlines())
        files = list_md_files(knowledge_file)
        md_files = [file for file in files if file not in existing_files]
        with open(output_file, 'a') as f:
            for file in md_files:
                f.write(file + '\n')
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)

    else:
        # 初始化知识库
        md_files = list_md_files(knowledge_file)
        save_to_txt(md_files, output_file)
        all_splits = ["我是人工智能也是护肤专家，你可以向我提问关于护肤的任何问题"]
        all_metadata = [{"Header 1": "你是谁", "Source": "introduce"}]
        vectorstore = Chroma.from_texts(texts=all_splits, metadatas=all_metadata, embedding=model,
                                        persist_directory=persist_directory)  # 标题和内容同时加载

    for file in md_files:
        all_splits,all_metadata = load_md_MHTS(knowledge_file,file)
        vectorstore.add_texts(texts=all_splits, metadatas=all_metadata)  # 向知识库添加内容

    vectorstore.persist()  # 向量数据库的持久化

    return vectorstore


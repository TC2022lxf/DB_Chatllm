import os

from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_community.vectorstores.chroma import Chroma
from utils.embedding_data import embedding_data
from utils.load_data import *
from config import DEFAULT_KNOWLEDGE_BASE

def chroma_data():
    '''
    向量数据库，使用chroma，直接用from_documents加载
    '''
    persist_directory = os.path.join('knowledge_base',DEFAULT_KNOWLEDGE_BASE)
    # embedding model
    model = embedding_data()
    # 检查持久化目录是否存在
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:  # 检查目录是否为空
        print("Chroma数据库已存在，无需重复创建.")
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=model)
    else:
        # 创建向量数据库
        docs = load_data()
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=model,
            persist_directory=persist_directory
        )
        vectordb.persist()  # 向量数据库的持久化

    return vectordb

def chroma_MHTS():
    '''
    使用自定义检索器，检索MarkdownTextSplitter方法分割的数据
    将content和metadata分开加载
    :return:
    '''
    persist_directory = os.path.join('knowledge_base', "chroma_MHTS")
    from utils.load_data import load_md_MHTS
    # embedding model
    model = embedding_data()
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:  # 检查目录是否为空
        print("Chroma数据库已存在，无需重复创建.")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
    else:
        # 创建向量数据库
        all_splits, all_metadatas = load_md_MHTS()  # 分割md文档，分为内容以及标题两部分
        vectorstore = Chroma.from_texts(texts=all_splits, metadatas=all_metadatas, embedding=model,
                                        persist_directory=persist_directory)  # 标题和内容同时加载
        vectorstore.persist()  # 向量数据库的持久化

    # Define our metadata
    metadata_field_info = [
        AttributeInfo(
            name="Header 4",
            description="这是一个概括内容的标题",
            type="string or list[string]",
        ),
    ]
    document_content_description = "关于各种如何变美的内容"  # 文档的描述
    # 打印向量数据库中的文档数量
    print(vectorstore._collection.count())
    return vectorstore,document_content_description,metadata_field_info

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
    加载有source的元数据。
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
        md_files = list_md_files(knowledge_file)
        save_to_txt(md_files, output_file)
        all_splits = ["我是人工智能也是护肤专家，你可以向我提问关于护肤的任何问题"]
        all_metadata = [{"Header 1": "你是谁", "Source": "introduce"}]
        vectorstore = Chroma.from_texts(texts=all_splits, metadatas=all_metadata, embedding=model,
                                        persist_directory=persist_directory)  # 标题和内容同时加载

    for file in md_files:
        all_splits,all_metadata = load_md_MHTS(knowledge_file,file)
        vectorstore.add_texts(texts=all_splits, metadatas=all_metadata)

    vectorstore.persist()  # 向量数据库的持久化

    return vectorstore

def add_chroma(persist_directory):
    # persist_directory = os.path.join('knowledge_base', "chroma_source")
    model = embedding_data()
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
    all_splits,all_metadata = load_md_MHTS()
    vectorstore.add_texts(texts=all_splits, metadatas=all_metadata)
    vectorstore.persist()
    return vectorstore

if __name__ == '__main__':
    add_chroma()
import os

from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_community.vectorstores.chroma import Chroma
from utils.embedding_data import embedding_data
from utils.load_data import load_data
from config import DEFAULT_KNOWLEDGE_BASE

def chroma_data():
    '''
    向量数据库，使用chroma
    '''
    persist_directory = os.path.join('knowledge_base',DEFAULT_KNOWLEDGE_BASE)
    docs = load_data()
    # embedding model
    model = embedding_data()
    # 检查持久化目录是否存在
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:  # 检查目录是否为空
        print("Chroma数据库已存在，无需重复创建.")
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=model)
    else:
        # 创建向量数据库
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
    :return:
    '''
    persist_directory = os.path.join('knowledge_base', "chroma_MHTS")
    from utils.load_data import load_md_MHTS
    # embedding model
    model = embedding_data()
    all_splits, all_metadatas = load_md_MHTS()  # 分割md文档，分为内容以及标题两部分
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:  # 检查目录是否为空
        print("Chroma数据库已存在，无需重复创建.")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=model)
    else:
        # 创建向量数据库
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
if __name__ == '__main__':
    chroma_data()
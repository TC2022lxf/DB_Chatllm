import json
import os
import re

from langchain.text_splitter import MarkdownTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from config import DEFAULT_DATA



def load_data():
    '''
    加载数据
    :param path: md文件路径
    :return:
    '''
    with open(doc_path, 'r', encoding='utf-8') as files:
        markdown_text = files.read()
    markdown_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = markdown_splitter.create_documents([markdown_text])  # 分割
    return docs


def load_docx() -> str:
    from langchain.document_loaders import Docx2txtLoader

    loader = Docx2txtLoader(doc_path)

    data = loader.load()
    return str(data[0].page_content)


def load_md_MHTS(doc_path):
    '''
    根据md文件的标题分割文档。
    :return:
    '''
    with open(doc_path, 'r', encoding='utf-8') as files:
        markdown_text = files.read()

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4")
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(markdown_text)

    # Char-level splits
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    chunk_size = 500
    chunk_overlap = 50
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # Split within each header group
    all_splits = []
    all_metadatas = []
    for header_group in md_header_splits:
        _splits = text_splitter.split_text(header_group.page_content)
        _metadatas = [header_group.metadata for _ in _splits]
        all_splits += _splits
        all_metadatas += _metadatas
    return all_splits,all_metadatas

def load_md_MHTS_source(doc_path,name):
    '''
    在上面函数的all_splits,all_metadatas基础上的元数据加上source来源
    :return:
    '''
    all_metadata = []
    path=doc_path+"/"+name
    all_splits, all_metadatas = load_md_MHTS(path)
    for i, metadata in enumerate(all_metadatas):  # 加source键
        new_metadata = metadata.copy()
        new_metadata["source"] = str(name.split(".")[0])
        all_metadata.append(new_metadata)
    to_json(doc_path,name.split(".")[0],all_splits,all_metadata)
    return all_splits,all_metadata

def to_json(path,name,all_splits,all_metadata):
    json_path = path+"/knowledge.json"
    print(json_path)
    combined_list = [{'page_content':content,'metadata':metadata} for content,metadata in zip(all_splits,all_metadata)]
    for i,m in enumerate(combined_list):
        print(i,m)

    if not os.path.exists(json_path):
        with open(json_path, 'w',encoding='utf-8') as json_file:
            json.dump(combined_list, json_file, ensure_ascii=False, indent=2)
    else:
        # 读取现有内容
        with open(json_path, 'r',encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        # 将新数据追加到现有内容中
        existing_data.append(combined_list)
        # 写入到文件中
        with open(json_path, 'w',encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    doc_path = os.path.join(DEFAULT_DATA, 'Skincare.md')



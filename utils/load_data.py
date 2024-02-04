import os

from langchain.text_splitter import MarkdownTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from config import DEFAULT_DATA

doc_path = os.path.join(DEFAULT_DATA, 'beautiful bible.md')
tpye = "docx"


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


def load_md_MHTS():
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
        _metadatas = [header_group.metadata for _ in _splits]  # 文本对应的标题
        all_splits += _splits
        all_metadatas += _metadatas
    return all_splits,all_metadatas


if __name__ == '__main__':
    doc_path = os.path.join(DEFAULT_DATA, 'beautiful bible.md')

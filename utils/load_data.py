import json
import os
import re

from langchain.text_splitter import MarkdownTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from modelscope import AutoTokenizer

from config import DEFAULT_DATA

# 分词器
tokenizer = AutoTokenizer.from_pretrained("qwen/Qwen-7B-Chat", trust_remote_code=True)

def length_function(text):
    return len(tokenizer.encode(text, add_special_tokens=False))



def load_md_MHTS(path,md_name):
    '''
    :param path:文件夹路径
    :param md_name: 文件夹内的md文件名
    :return: 分割后的文本列表
    '''
    md_path = path+'/'+md_name
    with open(md_path, 'r', encoding='utf-8') as files:
        markdown_text = files.read()

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6")
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(markdown_text)

    # Char-level splits
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    chunk_size = 500
    chunk_overlap = 50
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
                                                   length_function=length_function)

    # Split within each header group
    all_splits = []
    all_metadatas = []
    for header_group in md_header_splits:
        header_group.metadata['source']=md_path.split('/')[-1] # 添加来源为该md文件
        print(header_group)
        _splits = text_splitter.split_text(header_group.page_content) # 每个标题中的内容再次分割
        _metadatas = [header_group.metadata for _ in _splits]
        all_splits += _splits
        all_metadatas += _metadatas
    to_json(path, all_splits, all_metadatas)  # 保存到文件同一目录下，同一名为knowledge
    return all_splits, all_metadatas

def to_json(path, all_splits, all_metadata):
    '''
    记录该目录下的所有md文件内容
    :param path:
    :param all_splits:
    :param all_metadata:
    :return:
    '''
    json_path = path + "/knowledge.json"
    print(json_path)
    combined_list = [{'page_content': content, 'metadata': metadata} for content, metadata in
                     zip(all_splits, all_metadata)]
    for i, m in enumerate(combined_list):
        print(i, m)

    if not os.path.exists(json_path):
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(combined_list, json_file, ensure_ascii=False, indent=2)
    else:
        # 读取现有内容
        with open(json_path, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        # 将新数据追加到现有内容中
        existing_data.append(combined_list)
        # 写入到文件中
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

def read_json(json_path):
    '''
    读取json中的content和metadata形成两个列表
    :param json_path:
    :return:
    '''
    with open(json_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    page_contents = []
    metadatas = []
    # 遍历每个对象
    for item in data:
        # 将page_content添加到page_contents列表中
        page_contents.append(item["page_content"])
        # 将metadata添加到metadatas列表中
        metadatas.append(item["metadata"])
    return page_contents,metadatas


if __name__ == '__main__':
    path = '../data'
    load_md_MHTS(path,'Skincare.md')
    read_json('../data/knowledge.json')

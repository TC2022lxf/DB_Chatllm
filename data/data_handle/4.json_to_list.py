'''
将json转化成匹配langchain向量库的document list 格式。
'''

from langchain_text_splitters import RecursiveJsonSplitter
import json
from pathlib import Path
file_path='/FT/lxf/langGraph/23903-i00.json'  # 可直接接入md 2 json v2 后面
json_data = json.loads(Path(file_path).read_text())
def json_to_list(json_data):
    result = []

    def process_node(node, parent_title=None):
        # 提取当前节点的信息
        content = node.get("content", "")
        metadata = {
            "parent_title": parent_title,
            "title": node.get("title"),
            "level": node.get("level"),
            "unique_id": node.get("unique_id"),
            "parent_id": node.get("parent_id"),
        }
        result.append((content, metadata))

        # 递归处理子节点
        for child in node.get("children", []):
            process_node(child, node.get("title"))

    # 处理每一个顶级节点
    for item in json_data:
        process_node(item)
    doc_result = [Document(metadata=score,page_content=doc) for doc, score in result]

    return doc_result

# 对每一块进行递归分割
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(json_to_list(json_data))
print(doc_splits)

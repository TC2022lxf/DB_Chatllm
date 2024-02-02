# 使用的数据文本
DEFAULT_DATA = "data"

# 默认使用的知识库
DEFAULT_KNOWLEDGE_BASE = "chroma"  # 放在knowledge_base

# 默认的"Vector stores"（向量存储)类型是：Faiss  见 https://www.langchain.com.cn/modules/indexes/vectorstores/examples/faiss
DEFAULT_VS_TYPE = "Faiss"

# 默认搜索引擎：duckduckgo  见 https://www.langchain.com.cn/modules/agents/tools/examples/ddg
DEFAULT_SEARCH_TYPE = "duckduckgo"

# 文本分割器TEXTSPLITTER配置, 见 https://www.langchain.com.cn/modules/indexes/text_splitters/examples/markdown
text_splitter_dict = {
    "MarkdownHeaderTextSplitter": {
        "headers_to_split_on":
            [
                ("#", "head1"),
                ("##", "head2"),
                ("###", "head3"),
                ("####", "head4"),
            ]
    }
}

# TEXTSPLITTER名称 见 https://python.langchain.com.cn/docs/modules/data_connection/document_transformers/text_splitters/markdown_header_metadata
TEXT_SPLITTER = "MarkdownHeaderTextSplitter"

# Embedding模型定制词语的词表文件
EMBEDDING_KEYWORD_FILE = "embedding_keywords.txt"

from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from utils.db import chroma_data
from utils.llm import load_llm
vectordb = chroma_data()
# 定义元数据的过滤条件
metadata_field_info = [
    AttributeInfo(
        name="Header 4",
        description="用来描述标题内容的",
        type="string or List[string]",
    ),
    AttributeInfo(
        name="Header 1",
        description="用来描述标题内容的",
        type="string or List[string]",
    ),
    AttributeInfo(
        name="Header 3",
        description="用来描述标题内容的",
        type="string or List[string]",
    ),
    AttributeInfo(
        name="Header 2",
        description="用来描述标题内容的",
        type="string or List[string]",
    ),
]

# 创建SelfQueryRetriever
document_content_description = "各种如何变美的内容"
llm = load_llm()
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectordb,
    document_content_description,
    metadata_field_info,
    verbose=True
)
# 问题
question = "什么是肤质"

# 搜索相关文档
docs = retriever.get_relevant_documents(question)

# 打印结果中的元数据信息
for d in docs:
    print(d.page_content,d.metadata)
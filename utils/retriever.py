
from utils.db import chroma_data


def retrievers(query) -> list:
    '''
    :param query:
    :return: 列表
    '''
    vectordb = chroma_data()
    context = vectordb.max_marginal_relevance_search(query, k=3)  # 使用mmr检索，可过滤相似度高的文档
    print(len(context))
    print(context)
    return context


# 重写查询检索器
from langchain.retrievers.self_query.base import SelfQueryRetriever

'''
使用样例：
prompt_multi_query = PromptTemplate(
    input_variables=["question"],
    template="""
    * 你是一个问题要素提取并重写问题的助手，主要将原问题重写成4个新问题并用于检索\n
    * 你的任务流程是：\
    1. 提取用户问题的主题和焦点、目的和意图、事件和行动。返回的key为"主题"、"焦点"、"目的"、"意图"、"事件"和"行动"。\
    2. 对问题进行4次重写，要求这4个问题与原问题的相似度尽量高。返回的Key为"问题组",value为list，lists包含4个重写后的新问题\
    3. 输出一个json格式的字符串，格式为"问题组":["新问题1","新问题2","新问题3","新问题4"],"主题":"主题","焦点":"焦点","目的":"目的","意图":"意图","事件":"事件","行动":"行动"\



    * 以下是需要重写的原问题:

    {question}
    """,)

question_rewriter = prompt_multi_query | llm2json | JsonOutputParser()

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embedding,  # Ensure embedding is correct
)

retriever = CustomRetriever(
    vectorstore=vectorstore,
    k=3,
    question_rewriter = question_rewriter
)

result = retriever.invoke("dinosaur movie with rating less than 8")

'''
from langchain_core.retrievers import BaseRetriever
from typing import List,Any, Dict
from langchain_core.documents import Document
class CustomRetriever(BaseRetriever):

    vectorstore: Any  # 假设 vectorstore 是任意类型，实际类型应根据你的需要来定义
    k: int
    question_rewriter: Any  # 同样，这里的 Any 应该替换为实际的类型

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """
        Get documents relevant to the query and add score information.
        多查询、相似度、重排查询
        Args:
            query (str): The search query.

        Returns:
            List[Document]: List of documents with updated scores.
        """
        fused_scores = {}  # Document scores will be accumulated here

        # Generate multiple queries using question_rewriter
        query_dict = self._get_query_dict(query)

        query_list = [query] + query_dict.get("问题组", [])

        for q in query_list:
            docs, scores = zip(*self.vectorstore.similarity_search_with_score(q, k=3))

            for doc, score in zip(docs, scores):
                doc.metadata["score"] = score

            self._update_fused_scores(docs, scores, fused_scores)

        # Re-rank documents based on the new scores
        reranked_results = self._get_reranked_results(fused_scores)
        return reranked_results[:self.k*2]

    def _get_query_dict(self, query: str) -> Dict[str, Any]:
        """Generate query dictionary and handle potential errors."""
        try:
            query_dict = self.question_rewriter.invoke(query)
            if not isinstance(query_dict, dict) or "问题组" not in query_dict or not isinstance(query_dict["问题组"],
                                                                                                list):
                raise ValueError("Invalid query_dict format")
            return query_dict
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
            return {"问题组": []}

    def _update_fused_scores(self, docs: List[Document], scores: List[float],
                             fused_scores: Dict[str, Dict[str, float]]):
        """Update fused scores based on document scores and ranking."""
        doc_scores = {doc.page_content: doc.metadata for doc in docs}

        for rank, (doc, score) in enumerate(sorted(doc_scores.items(), key=lambda x: x[1]["score"], reverse=True)):
            if doc not in fused_scores:
                fused_scores[doc] = score
                fused_scores[doc]["score"] = 0
            fused_scores[doc]["score"] += 1.0 / (rank + 60)
            print(fused_scores[doc]["score"])

    def _get_reranked_results(self, fused_scores: Dict[str, Dict[str, float]]) -> List[Document]:
        """Re-rank documents based on the new scores."""
        return [Document(metadata=score, page_content=doc) for doc, score in
                sorted(fused_scores.items(), key=lambda x: x[1]["score"], reverse=True)]


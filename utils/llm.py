from langchain.chains import LLMChain, RetrievalQA, ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.retrievers import SelfQueryRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.outputs import LLMResult

from utils.prompt import *
from utils.retriever import retrievers
from config import LLM_MODELS,MODEL_PATH
from utils.db import *
class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.str = ''
        # 记得结束后这里置true
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        print(token)
        self.str +=token
        self.tokens.append(token)

    def on_llm_end(self, response: LLMResult, **kwargs: any) -> None:
        self.finish = 1

    def on_llm_error(self, error: Exception, **kwargs: any) -> None:
        print(str(error))
        self.tokens.append(str(error))

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                pass
def load_llm():
    # callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    # return LlamaCpp(model_path=MODEL_PATH['llm_model'][LLM_MODELS], callback_manager=callback_manager,
    #                 verbose=True, n_ctx=2048,temperature=0)
    from langchain_community.llms.ollama import Ollama
    from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

    llm = Ollama(base_url="http://localhost:11434",
                     model="qwen:7b",
                     callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                 )

    return llm
def llm(question:str,db,stream,history=[]):
    '''
    有提示的语言模型对话
    :param question:
    :return:
    '''
    knowledge_list=db
    return responde

def llm_MHTS_SQ(question):
    '''
    失败的语言模型辅助检索，能检索出来，但是无法执行后面两句话，无法回答
    见：https://python.langchain.com.cn/docs/modules/data_connection/document_transformers/text_splitters/markdown_header_metadata
    :param question:
    :return:
    '''
    llm = load_llm()

    vectorstore,document_content_description,metadata_field_info = chroma_MHTS()
    # Define self query retriver
    sq_retriever = SelfQueryRetriever.from_llm(llm, vectorstore, document_content_description, metadata_field_info,
                                               verbose=True)  # 自查询
    doc = sq_retriever.get_relevant_documents(question)  # 检索问题
    for d in doc:
        print(d.page_content, d.metadata)
    # print("question:"+question)
    # qa_chain = RetrievalQA.from_chain_type(llm, retriever=sq_retriever)  #根据检索内容，结合llm回答
    # qa_chain.run(question)

def llm_resource(question):
    '''
    返回source来源，目前不太需要，可搁置
    :param question:
    :return:
    '''
    docsearch = chroma_source()
    docs = docsearch.similarity_search(question)
    QUESTION_PROMPT, COMBINE_PROMPT = prompt5()
    chain = load_qa_with_sources_chain(load_llm(), chain_type="map_reduce", return_intermediate_steps=True,
                                       question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
    ## 加载的元数据要有source
    print(question)
    chain({"input_documents": docs, "question": question})
def compression_llm(question):
    '''
    将检索出来的结果用llm压缩，失败
    :param question:
    :return:
    '''
    llm = load_llm()
    vectordb = chroma_data()
    compressor = LLMChainExtractor.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vectordb.as_retriever()
    )
    compressed_docs = compression_retriever.get_relevant_documents(question)
    print(f"\n{'-' * 100}\n".join([f"Document {i + 1}:\n\n" + d.page_content for i, d in enumerate(compressed_docs)]))

class llm_QA_chains():
    '''
    根据检索出的结果，
    https://www.langchain.com.cn/modules/chains/index_examples/question_answering
    llm的问答，自定义提示，stuff链、map_reduce链、Refine链、map-rerank链、
    建议stuff和map-rerank
    无历史记录
    '''
    def __init__(self,question):
        self.docsearch = chroma_source()
        self.llm = load_llm()
        self.docs = self.docsearch.as_retriever().get_relevant_documents(question)
        self.question = question
        print(self.docs)

    def stuff(self):
        '''
        可行，效果还不错
        :return:
        '''
        chain = load_qa_chain(self.llm, chain_type="stuff", prompt=prompt1())
        qa = ConversationalRetrievalChain(
            retriever=self.docsearch.as_retriever(), combine_docs_chain=chain)
        qa({"input_documents": self.docs, "question": self.question}, return_only_outputs=True)

    def map_reduce(self):
        '''
        尝试用两个prompt，但是不知道如何设置，把握不好，回答太长，效果不好,后面可能再改改prompt
        两个prompt是question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT用prompt2()返回
        :return:
        '''
        QUESTION_PROMPT,COMBINE_PROMPT=prompt2()
        chain = load_qa_chain(self.llm, chain_type="map_reduce", return_map_steps=True,question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
        chain({"input_documents": self.docs, "question": self.question}, return_only_outputs=True)
        ##chain = load_qa_chain(OpenAI(temperature=0), chain_type="map_reduce", return_map_steps=True)  #检查中间过程
        ##chain({"input_documents": docs, "question": query}, return_only_outputs=True)

    def refine(self):
        '''
        同样的问题，答案太长太详细了。
        :return:
        '''
        refine_prompt,initial_qa_prompt = prompt3()
        chain = load_qa_chain(self.llm, chain_type="refine", return_refine_steps=True,
                              question_prompt=initial_qa_prompt, refine_prompt=refine_prompt)
        chain({"input_documents": self.docs, "question": self.question}, return_only_outputs=True)

    def map_rerank(self):
        '''
        这个根据prompt，我们让llm回答，并给回答打上分数，越高越相似，还凑合
        :return:
        '''
        chain = load_qa_chain(self.llm, chain_type="map_rerank", return_intermediate_steps=True,
                              prompt=prompt4())
        query = "What did the president say about Justice Breyer"
        chain({"input_documents": self.docs, "question": self.question}, return_only_outputs=True)

def chat_llm(question):
    from langchain.memory import ConversationBufferMemory
    vectorstore = chroma_source()
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # qa = ConversationalRetrievalChain.from_llm(load_llm(), vectorstore.as_retriever(), memory=memory)
    # result = qa({"question": question})  # 能回答，较短
    # result = qa({"question": "你知道我的朋友艾米是个什么博主吗"})  # 回答不知道，我认为没道理不知道
    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(load_llm(), vectorstore.as_retriever(), return_source_documents=True)

    result = qa({"question": question, "chat_history": chat_history})
    print("answer: ",result["answer"])
    print("source doc: ",result["source_documents"])
    chat_history = [(question, result["answer"])]
    result = qa({"question": "那我应该如何判断我的肤质好不好呢", "chat_history": chat_history})
    print("answer: ", result["answer"])
    chat_history.append((question, result["answer"]))
    print("source doc: ", result["source_documents"])
    print(chat_history)

def get_chat_history(inputs) -> str:
    res = []
    for human, ai in inputs:
        res.append(f"Human:{human}\nAI:{ai}")
    return "\n".join(res)

def stream_chat_llm(question):
    _template = """将输入的问题整理一下，去除多余的废话，使其更加整洁干净
    输入问题: {question}
    干净的问题:"""
    CONDENSE_QUESTION_PROMPT = PromptTemplate(
        template=_template, input_variables=["question"]
    )

    prompt_template = """使用以下上下文和聊天历史记录来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案.

    上下文: {context}
    
    聊天历史记录: {chat_history}
    
    问题: {question}
    有帮助的答案:"""
    QA_PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context","chat_history", "question"]
    )

    llm = load_llm()
    docsearch = chroma_source()
    #docs= docsearch.similarity_search(question)
    question_generator = LLMChain(llm=llm,prompt=CONDENSE_QUESTION_PROMPT)
    chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_PROMPT)
    qa = ConversationalRetrievalChain(
        retriever=docsearch.as_retriever(), combine_docs_chain=chain, question_generator=question_generator, return_source_documents=True)
    chat_history = []
    qa.stream({"question": question, "chat_history": chat_history}, return_only_outputs=True)
    result = qa({"question": question, "chat_history": chat_history}, return_only_outputs=True)
    chat_history.append((question,"艾米是个美妆博主",result["answer"]))
    query = "你知道艾米是做什么工作的吗？"
    result2 = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query,result2["answer"]))
    print(chat_history)

if __name__ == '__main__':
    print(MODEL_PATH['llm_model'][LLM_MODELS])

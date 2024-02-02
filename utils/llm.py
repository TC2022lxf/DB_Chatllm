from langchain.chains import LLMChain, RetrievalQA
from langchain.retrievers import SelfQueryRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from utils.prompt import *
from utils.retriever import retrievers
from config import LLM_MODELS,MODEL_PATH
from utils.db import *
def load_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    return LlamaCpp(model_path=MODEL_PATH['llm_model'][LLM_MODELS], callback_manager=callback_manager,
                    verbose=True, n_ctx=2048,temperature=0)

def llm_no_prompt(question):
    '''
    没有提示的，语言模型对话
    :param question:
    :return:
    '''
    prompt = create_prompt_template_no_context()
    # context = retrievers(question)
    llm_chain = LLMChain(prompt=prompt, llm=load_llm())
    responde = llm_chain.run(question=question)
    return responde

def llm(question):
    '''
    有提示的语言模型对话
    :param question:
    :return:
    '''
    prompt = create_prompt_template()
    context = retrievers(question)
    context = str(context[0].page_content)
    print(context)
    llm_chain = LLMChain(prompt=prompt, llm=load_llm())
    responde = llm_chain.run(context=context,question=question)
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

def prompt_template_CRQA(self):
    '''
    根据检索出的结果，
    构建llm-prompt提示词模板,创建新的检索方式实现对话式QA
    '''
    retrievers()
    create_prompt_template()

    '''
    对话式问答QA，基于问答QA，后面再写
    '''
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # qa = ConversationalRetrievalChain.from_llm(llm, vectordb.as_retriever(), memory=memory)
    '''
    问答QA
    '''


def prompt_template_QA(self):
    self.chroma_data()
    self.load_llm()
    query = self.query
    '''
    第一种代码：
    '''
    prompt_template = """我将给你一个知识文本context,以及一个与你的工作有关的问题question.
    如果你在context中无法搜寻到问题的答案,即使你本身知道答案但我也请你不要回答,只需要告诉我你不知道答案就行.
    知识文本为:{context},
    问题为:{question}
    """
    # PROMPT = PromptTemplate(
    #     template=prompt_template, input_variables=["context", "question"]
    # )
    # # 自定义 chain prompt
    # chain_type_kwargs = {"prompt": self.prompt}
    # qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.vectordb.as_retriever(search_type="mmr"),
    #                                  chain_type_kwargs=chain_type_kwargs)
    # print(qa.run(query))
    #
    # '''
    # 第二种代码,传上了input_documents为检索知识库出的内容
    # '''
    # self.retrievers()
    # chain = load_qa_chain(self.llm, chain_type="stuff", prompt=PROMPT)
    # answer = chain({"input_documents": self.doc, "question": query}, return_only_outputs=True)
    # print(answer)

    '''
    第三种代码,契合llamacpp的
    '''
    doc = retrievers(query)
    create_prompt_template()
    llm_chain = LLMChain(prompt=self.prompt, llm=self.llm)
    context = repr(doc[0].page_content)
    answer = llm_chain.run(context=context, question=query)
    print(answer)



if __name__ == '__main__':
    print(MODEL_PATH['llm_model'][LLM_MODELS])

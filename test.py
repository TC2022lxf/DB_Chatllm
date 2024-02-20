from langchain.chains import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms.ollama import Ollama

from utils.db import *
from utils.load_data import *
from utils.llm import *
from utils.prompt import *


def data_splitter_test():
    '''
    根据标题分割内容测试，目前稳定
    :return:
    '''
    all_splits, all_metadata = load_md_MHTS_source()
    for split, metadata in zip(all_splits, all_metadata):
        print(f"{metadata}\n{split}\n\n")


def search_question(question):
    '''
    根据问题从数据库检索数据的测试，目前稳定
    :return:
    '''
    from utils.llm import load_llm
    vectordb, document_content_description, metadata_field_info = chroma_MHTS()
    docs = vectordb.similarity_search(question)
    print(question)
    print(docs)
    return docs


def llm_context_test(question):
    '''
    检测语言模型在有context时回答的效果,连续运行五次，相对稳定，时而回答少时而回答多，但内容近似
    :param question:
    :return:
    '''
    context = "简单地说，肤质是皮肤的外观、触感和特性的描述。化妆品公司通常将肤质分为四大类，不过这种分类经常没用：1\.中性肤质\(皮肤没有出油或干燥的区城\)2\.油性肤质\(整个脸部的皮肤都很油，完全没有干燥的区城\)3\.干性肤质\(皮肤干燥紧绷，甚至有些脱皮，完全没有出油的区城\)4\.混合性肤质\(T字部位出油，其他部位是中性或干性肤质\)通常青春痘肤质被归类为油性或混合性皮肤，有时候也会单独被归类为一种肤质。敏感性皮肤有时也会单独被归类为一种肤质。 这四种或六种皮肤分类看起来是面面俱到了，其实肤质没有这么简单，这也是很多人搞不清自己究竟属于哪一种肤质的原因。"
    llm = load_llm()
    prompt = create_prompt_template()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    llm_chain.run(context=context, question=question)


def llm_no_context(question):
    '''
    检测语言模型在无context时的回答,此回答根据llm自身功能，回答的十分详细，说明llm自身就明白这个问题如何回答。
    :param question:
    :return:
    '''
    from utils.llm import load_llm
    llm = load_llm()
    prompt = create_prompt_template_no_context()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    llm_chain.run(question=question)



if __name__ == '__main__':
    # data_splitter_test()
    question = "我有个朋友，叫做艾米，是个美妆博主，她想知道如何让她的肤质变好"
    # llm_no_context(question)
    # source(question)
    #llm_QA_chains(question).stuff()
    #chat_llm(question)
    #data_splitter_test()
    stream_chat_llm(question)

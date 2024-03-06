from langchain.chains import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.text_splitter import CharacterTextSplitter
from modelscope import snapshot_download, AutoTokenizer, AutoModelForCausalLM


#from langchain_community.llms.ollama import Ollama



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
    #data_splitter_test()
    question = "hello"
    # llm_no_context(question)
    # source(question)
    #llm_QA_chains(question).stuff()
    #chat_llm(question)
    #data_splitter_test()
    #stream_chat_llm(question)
    #retrievers(question)
    #chroma_source()
    #to_json()
    #print(list_file("data"))
    #chroma_source("knowledge_base/test")
    # from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
    # from qstart import  Ollama
    # llm = Ollama(base_url="http://localhost:11434",
    #              model="qwen:7b",
    #              callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    #              )
    # llm.invoke(question)
    #text="肉毒杆菌是一种生长在缺氧环境下的细菌，在罐头食品及密封腌渍食物中具有极强的生存能力，是毒性最强的细菌之一。肉毒杆菌是一种致命病菌，在繁殖过程中分泌肉毒毒素，该种毒素是已知的最剧毒物，可抑制胆碱能神经末梢释放乙酰胆碱，导致肌肉松弛型麻痹。军队常常将这种毒素用于生化武器。人们食入和吸收这种毒素后，神经系统将遭到破坏，出现眼睑下垂、复视、斜视、吞咽困难、头晕、呼吸困难和肌肉乏力等症状，严重者可因呼吸麻痹而死亡。  \n科学家和美容学家正是看中了肉毒杆菌毒素能使肌肉暂时麻痹这一功效。医学界原先将该毒素用于治疗面部痉挛和其他肌肉运动紊乱症，用它来麻痹肌肉神经，以此达到停止肌肉痉挛的目的。可在治疗过程中，医生们发现它在消除皱纹方面有着异乎寻常的功能，其效果远远超过其他任何一种化妆品或整容术。因此，利用肉毒杆菌毒素消除皱纹的整容手术应运而生，并因疗效显著而在很短的时间内就风靡整个美国。"
    text = "我我我我我我我我我我我我"
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-7B-Chat")
    print(len(tokenizer.encode(text, add_special_tokens=False)))

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

template = """
Context: {context}
Question: {question}
Answer:"""
context = "简单地说，肤质是皮肤的外观、触感和特性的描述。化妆品公司通常将肤质分为四大类，不过这种分类经常没用：1\.中性肤质\(皮肤没有出油或干燥的区城\)2\.油性肤质\(整个脸部的皮肤都很油，完全没有干燥的区城\)3\.干性肤质\(皮肤干燥紧绷，甚至有些脱皮，完全没有出油的区城\)4\.混合性肤质\(T字部位出油，其他部位是中性或干性肤质\)通常青春痘肤质被归类为油性或混合性皮肤，有时候也会单独被归类为一种肤质。敏感性皮肤有时也会单独被归类为一种肤质。 这四种或六种皮肤分类看起来是面面俱到了，其实肤质没有这么简单，这也是很多人搞不清自己究竟属于哪一种肤质的原因，为什么会这样呢?皮肤随时在改变，它不会永远停留在同一种肤质里面。了解自己的皮肤特性很重要，肤质绝不是化妆品公司的分。"
prompt = PromptTemplate(template=template, input_variables=["context", "question"])
# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="llm_model_gguf/ggml-model-q4_0.gguf",
    callback_manager=callback_manager,
    verbose=True,
    n_ctx=2048,
    use_mlock=True,
    n_gpu_layers=12,
    n_threads=4,
    n_batch=1000
)
llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "什么是肤质?"
answer = llm_chain.run(context=context, question=question)
print(answer)

# from langchain.llms import LlamaCpp
# from langchain import PromptTemplate, LLMChain
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from utils.llm import llm
# template = """
#
# Question: {question}
#
# Answer: """
# prompt = PromptTemplate(template=template, input_variables=[])
# # Callbacks support token-wise streaming
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# # Verbose is required to pass to the callback manager
#
# # Make sure the model path is correct for your system!
#
# question = "什么是肤质?"
# llm_chain = llm(question)
#
# from langchain_community.llms.ollama import Ollama
# from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
#
# llm = Ollama(base_url="http://localhost:11434",
#                  model="qwen",
#                  callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
#
# llm.invoke("你好")

from utils.db import chroma_MHTS
from utils.llm import *
from utils.load_data import load_md_MHTS
from utils.retriever import *
llm("什么是肤质")



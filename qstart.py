import sys

from langchain_community.llms.ollama import Ollama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.outputs import LLMResult
from loguru import logger

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.str = ''
        # 记得结束后这里置true
        self.finish = False
    def on_llm_new_token(self, token: str, **kwargs):
        self.str +=token
    def on_llm_end(self, response: LLMResult, **kwargs: any) -> None:
        logger.info("123")
        """Run when LLM ends running."""
llm = Ollama(base_url="http://localhost:11434",
                 model="qwen:7b",
                 callback_manager=CallbackManager([ChainStreamHandler()]),
             )
llm.stream("hello")
# import logging
# from datetime import datetime
#
# # 配置日志记录器
# logging.basicConfig(level=logging.INFO)
#
# def add_timestamp_to_stream(stream_func):
#     def wrapper(*args, **kwargs):
#         logger = logging.getLogger(__name__)  # 获取当前模块的日志记录器
#         for token in stream_func(*args, **kwargs):
#             timestamp = datetime.now()  # 获取当前时间戳
#             logger.info(f"Token: {token}, Timestamp: {timestamp}")  # 使用 logger.info 记录时间戳
#             yield token
#     return wrapper
#
# # 使用装饰器包装 stream 函数
# stream_with_timestamp = add_timestamp_to_stream(llm.stream)

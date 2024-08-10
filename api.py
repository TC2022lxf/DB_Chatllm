import datetime
import time
from typing import Optional

import requests
import uvicorn
from fastapi import FastAPI
from langchain_community.chat_models import ChatOllama
from langchain_community.llms.ollama import Ollama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import LLMResult
from typing import TYPE_CHECKING, Any, Dict, List
from utils.embedding_data import embedding_data
from langchain_community.vectorstores.chroma import Chroma
from sse_starlette import EventSourceResponse
from loguru import logger
app = FastAPI()
global_history_dict={}
user_id,chat_id,question="sss"
logger.add(f"logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.log", rotation="500 MB")
def load_db(persist_directory="knowledge_base/chroma"):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_data())
    logger.info("知识库加载成功")
    return vectorstore
global t_id
def load_llm():
    class StreamingStdOutCallbackHandler_log(StreamingStdOutCallbackHandler):
        def __init__(self):
            self.str = ''
        def on_llm_new_token(self, token: str, **kwargs):
            logger.info(f"新的token:{token}")
            self.str += token
        def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
            logger.info("最后一个token生成结束")
            logger.info(f"答案生成完毕：{self.str}")

    llm = ChatOllama(base_url="http://localhost:11434",model="qwen:7b",callback_manager=CallbackManager([StreamingStdOutCallbackHandler_log()]))
    return llm

def record_all_history(user_id:str,chat_id:str,question:str,answer:str):
    global global_history_dict
    if user_id not in global_history_dict: global_history_dict[user_id]={}
    if chat_id not in global_history_dict[user_id]: global_history_dict[user_id][chat_id]=[]
    global_history_dict[user_id][chat_id]+=[HumanMessage(content=question),AIMessage(content=answer)]
    logger.info(f"总history记录为：{global_history_dict}")
    logger.info("总history记录完毕")

def find_id_history(user_id:str,chat_id:str):
    global global_history_dict
    if user_id not in global_history_dict or chat_id not in global_history_dict[user_id]:
        id_history_list=[]
        logger.info(f"用户id:{user_id},聊天id:{chat_id},无聊天记录")
    else :
        id_history_list=global_history_dict[user_id][chat_id]
        logger.info(f"用户id:{user_id},聊天id:{chat_id},查找完毕")
    return id_history_list

def input_message(question:str,db,history=[]):
    knowledge=db.max_marginal_relevance_search(question,k=3)
    logger.info("知识检索完毕")
    chat_history = [
        SystemMessage(
            content="你是一个化妆品方向的专家，你的职责是用50字以内专业化的口语回答用户的问题。如果检索到的知识与用户无关，可以忽略，直接自然流畅地回答就好。"),
        HumanMessage(content=question),
        SystemMessage(content=f"检索到相关知识:{knowledge}")
    ]
    if history:
        chat_history=[
                           SystemMessage(
                               content="你是一个化妆品方向的专家，你的职责是用100字以内专业化的口语回答用户的问题。系统有时检索到的知识与用户提出的问题无关，可以忽略，直接自然流畅地回答就好。"),
                       ] + history + [
                           HumanMessage(content=question),
                           SystemMessage(content=f"检索到相关知识:{knowledge}")
                       ]
        logger.info(f"历史记录如下：\n{chat_history}")
    else:
        logger.info(f"message如下：{chat_history}")
    return chat_history

@app.post("/stream/{user_id}",summary="基于知识库的流式回答",description="参数user_id是用户唯一的id,chat_id是用户不同聊天记录唯一的id")
def qa_with_kb_api(user_id:str,chat_id:str,question:str,stream:Optional[bool]=False):
    def generator(generators):
        string = ""
        for item in generators:
            string+=item.content
            yield item
        record_all_history(user_id, chat_id, question,string)
    llm=load_llm()
    history=find_id_history(user_id,chat_id)
    message=input_message(question,load_db(),history)
    logger.info(f"问题:{question}.答案开始生成")
    if(stream):
        answer=llm.stream(message)
        return EventSourceResponse(generator(answer), media_type="text/event-stream")
    else:
        answer=llm.invoke(message).content
        record_all_history(user_id, chat_id, question, answer)
        return answer

if __name__ == '__main__':
    # from langchain_anthropic import ChatAnthropic
    #uvicorn.run(app, host="0.0.0.0", port=8502, workers=1)
    # record_all_history("1","1","hello","answer")
    # print(global_history_dict)
    # Use a pipeline as a high-level helper
    # index
    # 模型下载
    # 模型下载

    # Copyright (c) Microsoft Corporation. All rights reserved.
    # Licensed under the MIT License.

    # -*- coding: utf-8 -*-

    import json

    from collections import deque
    queue = deque()
    queue.append(1)
    queue.append(2)
    print(queue)
    queue.pop()
    print(queue)
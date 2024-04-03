# import requests
#
# headers = {
#     'Content-Type': 'application/json',
# }
# #"model" : "phi"
# #"model" : "llama2"
# #"model" : "mistral"
#
# data = '{\n  "model": "qwen:7b",\n  "prompt": "Why is the sky blue? Is it related to sunshine?",\n  "stream": True,\n  "keep_alive":"24h"}'
#
# response = requests.post('http://localhost:11434/api/generate', headers=headers, data=data)
# jsonResponse = response.json()
# #print(jsonResponse)
#
# model = ""
# total_duration = 0.0
# load_duration = 0.0
# prompt_eval_count = 0
# prompt_eval_duration = 0.0
# eval_count = 0
# eval_duration = 0.0
# for key, value in jsonResponse.items():
#     if (key=="response"):
#         pass
#     elif (key=="context"):
#         pass
#     elif (key=="model"):
#         model = value
#     elif (key=="total_duration"):
#         total_duration = float(value)/(10**6)
#     elif (key=="load_duration"):
#         load_duration = float(value)/(10**6)
#     elif (key=="prompt_eval_count"):
#         prompt_eval_count=int(value)
#     elif (key=="prompt_eval_duration"):
#         prompt_eval_duration=float(value)/(10**6)
#     elif (key=="eval_count"):
#         eval_count=int(value)
#     elif (key=="eval_duration"):
#         eval_duration=float(value)/(10**6)
#
# print(f"model = {model}")
#
# print(f"{'total_duration time': >20} = {total_duration:10.2f} ms")
# print(f"{'load_duration time': >20} = {load_duration:10.2f} ms")
#
# print(f"{'prompt eval time ': >20} = {prompt_eval_duration:10.2f} ms / {prompt_eval_count:>6} tokens")
# print(f"{'eval time ': >20} = {eval_duration:10.2f} ms / {eval_count:>6} tokens ")
# print(f"Performance: {eval_count/eval_duration*1000:10.2f}(tokens/s)")
#
import requests
import json

import requests
import time
from datetime import datetime
import pytz
from loguru import logger
def get_bj_time():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

def load_model_time():
    model_name  ="qwen:7b"
    logger.info(f"{model_name}模型加载时间")
    while True:
        data = {"model": model_name, "keep_alive": "5m"}
        headers = {'Content-Type': 'application/json'}
        high_precision_time = time.perf_counter()
        response = requests.post('http://localhost:11434/api/generate', json=data, headers=headers)
        high_precision_time_end = time.perf_counter()
        time1 = high_precision_time_end-high_precision_time
        print(f"高精度时间（精确到微秒）: {time1*1000:.6f}")
        jsonResponse = response.content.decode('utf-8')  # 将 bytes 转换为字符串以便打印
        print(jsonResponse)
        print(f"当前北京时间：{get_bj_time()}")
        time.sleep(280)  # 暂停280秒后再次执行

        '''
        7b初次加载模型时间：3.867187177s， 第二次加载模型时间：0.766666ms
        14b初次加载模型时间：5.180146173s , 第二次加载模型时间：0.753414ms
        72b初次加载模型时间：16.991763358s，第二次加载模型时间：1.358505ms
        
        '''
def benchmarking_token():
    model_name="qwen:7b"
    question='hello'
    data = {"model": model_name, "prompt":question,"keep_alive": "5m","stream": False}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:11434/api/generate', json=data, headers=headers)
    json_data = json.loads(response.text)
    eval_count = json_data["eval_count"]
    eval_duration = json_data["eval_duration"]
    # 计算每秒令牌生成数
    tokens_per_second = eval_count / (eval_duration / 1e9)
    print("token数：",eval_count)
    print("token生成时间", (eval_duration / 1e6),"ms")
    print("每秒token生成数:", tokens_per_second)

if __name__ == '__main__':

    #load_model_time()
    benchmarking_token()


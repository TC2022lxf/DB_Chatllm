import os

# 选用的 Embedding 名称
EMBEDDING_MODEL = "bge-large-zh"

# Embedding 模型运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
EMBEDDING_DEVICE = 'cpu'

# llm语言模型
LLM_MODELS = "qwen-1_8B-gguf"

# LLM 运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
LLM_DEVICE = "auto"

# 大模型最长支持的长度，如果不填写，则使用模型默认的最大长度，如果填写，则为用户设定的最大长度
MAX_TOKENS = None

# LLM通用对话参数
TEMPERATURE = 0.7

MODEL_PATH = {
    "embed_model": {
        "bge-large-zh": "model/embedding_model/bge-large-zh"
    },
    "llm_model": {
        "qwen-1_8B-gguf": "model/llm_model_gguf/ggml-model-q4_0.gguf"
    }
}

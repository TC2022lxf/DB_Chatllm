from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig
from transformers import set_seed
def _get_input() -> str:
    while True:
        try:
            message = input('用户 > ').strip()
        except UnicodeDecodeError:  # 输入包含无法解码的字符
            print('[ERROR] Encoding error in input')
            continue
        except KeyboardInterrupt:  # 按下 Ctrl+C 导致 KeyboardInterrupt 异常
            exit(1)
        if message:  # Not NULL
            return message
        print('[ERROR] Query is empty')

def get_model_and_tok():
    # 加载预训练模型的tokenizer
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-1_8B-Chat", revision='master', trust_remote_code=True)

    # 加载预训练的模型Qwen 1.8B
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-1_8B-Chat", device_map="auto",
                                                 trust_remote_code=True).eval()
    # 从预训练模型“Qwen/Qwen-1_8B-Chat”加载生成任务的配置信息，如最大生成长度、温度控制、top_k采样等
    config = GenerationConfig.from_pretrained("Qwen/Qwen-1_8B-Chat", trust_remote_code=True, resume_download=True, )
    return model,tokenizer,config

if __name__ == '__main__':

    model, tokenizer,config = get_model_and_tok()


    history, response = [], ''

    while True:
        query = _get_input()
        '''
        可实现输入的功能：
        :help / :h          Show this help message              显示帮助信息
            :exit / :quit / :q  Exit the demo                       退出Demo
            :clear / :cl        Clear screen                        清屏
            :clear-his / :clh   Clear history                       清除对话历史
            :history / :his     Show history                        显示对话历史
            :seed               Show current random seed            显示当前随机种子
            :seed <N>           Set random seed to <N>              设置随机种子
            :conf               Show current generation config      显示生成配置
            :conf <key>=<value> Change generation config            修改生成配置
            :reset-conf         Reset generation config             重置生成配置
        '''

        # Run
        seed = 1234
        set_seed(seed)
        """
        TextIteratorStreamer实现流式输出模块
        ...
        TextStreamer实现流式输出模块
        ...
        """
        # 返回模型的响应
        for response in model.chat(tokenizer,query,history=history,callaback = [StreamingStdOutCallbackHandler()],generation_config=config):
            print(f"\n用户:{query}")
            print(f"\n千问:{response}")
        history.append((query,response))
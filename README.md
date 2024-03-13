# 环境配置
```bash
pip install requirements.txt -r
```

# 配置语言模型
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen:7b
```

# 快速开始
```bash
streamlit run web_demo.py
```

# 页面展示
![img.png](pages/img.png)
主页面web demo用来配置语言模型的参数以及选择知识库
![img_1.png](pages/img_1.png)
![img_2.png](pages/img_2.png)
可创建或继续添加知识进入知识库中

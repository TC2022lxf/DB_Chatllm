# 环境配置
```bash
pip install requirements.txt -r
```

# 配置语言模型
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen:7b
```
## 关于ollama面向多用户应用级并发的做法
https://zhuanlan.zhihu.com/p/691506962
docker+Nginx+Ollama（Linux）使用ollama并发
# 快速开始
为主页面的入口，副页面为pages文件下的三个代码
```bash
streamlit run web_demo.py
```

# 页面展示
![img.png](pages/img.png)
主页面web demo用来配置语言模型的参数以及选择知识库
![img_1.png](pages/img_1.png)
![img_2.png](pages/img_2.png)
可创建或继续添加知识进入知识库中

# 数据处理

data/data_handle下的docx_to_md.py文件可以支持将带有标题、表格、图片的docx文档转化成md格式<p>
md_to_json.py可以将md格式根据标题分级划分，每个子标题内容都会根据llm总结内容并添加到父标题。保存成json格式，结构如下：
```bash
{
    "Title 1": {
        "parent": None,
        "content": ["Content 1 Content 1.1 Content 1.1.1"],
        "Subtitle 1.1": {
            "parent": "Title 1",
            "content": ["Content 1.1 Content 1.1.1"],
            "Sub-subtitle 1.1.1": {
                "parent": "Subtitle 1.1",
                "content": ["Content 1.1.1"]
            }
        }
    },
    "Title 2": {
        "parent": None,
        "content": ["Content 2"]
    }
}
```

# 待补充
模型个性化<p>
RAG多样化尝试
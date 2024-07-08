# 基础
## 目前 主流的开源模型体系 有哪些？
- Llama
- Qwen
- ChatGLM
- mixtral
- deepspeek
## prefix Decoder 和 causal Decoder 和 Encoder-Decoder 区别是什么？
## 大模型LLM的 训练目标 是什么？
## 涌现能力是啥原因？
## 为何现在的大模型大部分是Decoder only结构？
## 简单 介绍一下 大模型【LLMs】？
## 大模型【LLMs】后面跟的 175B、60B、540B等 指什么？
## 大模型【LLMs】具有什么优点？
## 大模型【LLMs】具有什么缺点？

# 进阶
## LLMs 复读机问题
### 什么是 LLMs 复读机问题？
### 为什么会出现 LLMs 复读机问题？
### 如何缓解 LLMs 复读机问题？
## llama 系列问题
### llama 输入句子长度理论上可以无限长吗？
## 什么情况用Bert模型，什么情况用LLaMA、ChatGLM类大模型，咋选？
## 各个专业领域是否需要各自的大模型来服务？
## 如何让大模型处理更长的文本？

# 微调
## 如果想要在某个模型基础上做全参数微调，究竟需要多少显存？
## 为什么SFT之后感觉LLM傻了?
## SFT 指令微调数据 如何构建?
## 领域模型Continue PreTrain 数据选取？
## 领域数据训练后，通用能力往往会有所下降，如何缓解模型遗忘通用能力？
## 领域模型Continue PreTrain ，如何 让模型在预训练过程中就学习到更多的知识？
## 进行SFT操作的时候，基座模型选用Chat还是Base?
## 领域模型微调 指令&数据输入格式 要求？
## 领域模型微调 领域评测集 构建？
## 领域模型词表扩增是不是有必要的？
## 如何训练自己的大模型？
## 训练中文大模型有啥经验？
## 指令微调的好处？
## 预训练和微调哪个阶段注入知识的？
## 想让模型学习某个领域或行业的知识，是应该预训练还是应该微调？
## 多轮对话任务如何微调模型？
## 微调后的模型出现能力劣化，灾难性遗忘是怎么回事？
## 微调模型需要多大显存？
## 大模型LLM进行SFT操作的时候在学习什么？
## 预训练和SFT操作有什么不同
## 样本量规模增大，训练出现OOM错
## 大模型LLM进行SFT 如何对样本进行优化？
## 模型参数迭代实验
## 微调大模型的一些建议

# 训练经验
## 分布式训练框架选择？
## LLMs 训练时 有哪些有用的建议？
## 模型大小如何选择？
## 加速卡如何选择？

# langchian
## 什么是 LangChain?
## LangChain 包含哪些 核心概念？
### 2.1 LangChain 中 Components and Chains 是什么？
### 2.2 LangChain 中 Prompt Templates and Values 是什么？
### 2.3 LangChain 中 Example Selectors 是什么？
### 2.4 LangChain 中 Output Parsers 是什么？
### 2.5 LangChain 中 Indexes and Retrievers 是什么？
### 2.6 LangChain 中 Chat Message History 是什么？
### 2.7 LangChain 中 Agents and Toolkits 是什么？
## 什么是 LangChain Agent?
## 如何使用 LangChain ?
## LangChain 支持哪些功能?
## 什么是 LangChain model?
## LangChain 包含哪些特点?
## LangChain 如何使用?
### 8.1 LangChain 如何调用 LLMs 生成回复？
### 8.2 LangChain 如何修改 提示模板？
### 8.3 LangChain 如何链接多个组件处理一个特定的下游任务？
### 8.4 LangChain 如何Embedding & vector store？
## LangChain 存在哪些问题及方法方案？
### LangChain 低效的令牌使用问题
### LangChain 文档的问题
### LangChain 太多概念容易混淆，过多的“辅助”函数问题
### LangChain 行为不一致并且隐藏细节问题
### LangChain 缺乏标准的可互操作数据类型问题
### LangChain 替代方案？

# langchain经验
## 一、基于LLM+向量库的文档对话 基础面

### 1.1 为什么 大模型 需要 外挂(向量)知识库？
### 1.2. 基于LLM+向量库的文档对话 思路是怎么样？
### 1.3. 基于LLM+向量库的文档对话 核心技术是什么？
### 1.4. 基于LLM+向量库的文档对话 prompt 模板 如何构建？
## 二、基于LLM+向量库的文档对话 存在哪些痛点？

## 三、基于LLM+向量库的文档对话 工程示例面

# llm文档对话-pdf
## 一、为什么需要进行pdf解析？

## 二、为什么需要 对 pdf 进行解析？

## 三、pdf解析 有哪些方法，对应的区别是什么？

## 四、pdf解析 存在哪些问题？

## 五、如何 长文档（书籍）中关键信息？

## 六、为什么要提取标题甚至是多级标题？

## 七、如何提取 文章标题？

## 八、如何区分单栏还是双栏pdf？如何重新排序？

## 九、如何提取表格和图片中的数据？

## 十、基于AI的文档解析有什么优缺点？

# 高效微调PEFT
## 微调方法是啥？如何微调？

## 为什么需要 PEFT？

## 介绍一下 PEFT？

## PEFT 有什么优点？

## 微调方法批处理大小模式GPU显存速度？

## Peft 和 全量微调区别？

## 多种不同的高效微调方法对比

## 当前高效微调技术存在的一些问题

## 高效微调技术最佳实践

## PEFT 存在问题？

## 能不能总结一下各种参数高效微调方法？

# 适配器微调 adapter-tuning
## 一、为什么 需要 适配器微调（Adapter-tuning）？

## 二、适配器微调（Adapter-tuning）思路？

## 三、 适配器微调（Adapter-tuning）特点是什么？

## 四、AdapterFusion 思路 是什么？

## 五、AdapterDrop 思路 是什么？

## 六、AdapterDrop 特点 是什么？

## 七、MAM Adapter 思路 是什么？

## 八、MAM Adapter 特点 是什么？

# 提示学习 prompting
## 一、为什么需要 提示学习（Prompting）？

## 二、什么是 提示学习（Prompting）？

## 三、提示学习（Prompting） 有什么优点？

## 四、提示学习（Prompting）有哪些方法，能不能稍微介绍一下它们间？

## 4.1 前缀微调（Prefix-tining）篇
### 4.1.1 为什么需要 前缀微调（Prefix-tining）？
### 4.1.2 前缀微调（Prefix-tining）思路是什么？
### 4.1.3 前缀微调（Prefix-tining）的优点是什么？
### 4.1.4 前缀微调（Prefix-tining）的缺点是什么？
## 4.2 指示微调（Prompt-tuning）篇
### 4.2.1 为什么需要 指示微调（Prompt-tuning）？
### 4.2.2 指示微调（Prompt-tuning）思路是什么？
### 4.2.3 指示微调（Prompt-tuning）优点是什么？
### 4.2.4 指示微调（Prompt-tuning）缺点是什么？
### 4.2.5 指示微调（Prompt-tuning）与 Prefix-tuning 区别 是什么？
### 4.2.6 指示微调（Prompt-tuning）与 fine-tuning 区别 是什么？
## 4.3 P-tuning 篇
### 4.3.1 为什么需要 P-tuning？
### 4.3.2 P-tuning 思路是什么？
### 4.3.3 P-tuning 优点是什么？
### 4.3.4 P-tuning 缺点是什么？
## 4.4 P-tuning v2 篇
### 4.4.1 为什么需要 P-tuning v2？
### 4.4.2 P-tuning v2 思路是什么？
### 4.4.3 P-tuning v2 优点是什么？
### 4.4.4 P-tuning v2 缺点是什么？

# LoRA
## 一、LoRA篇

### 1.1 什么是 LoRA？
### 1.2 LoRA 的思路是什么？
### 1.3 LoRA 的特点是什么？
## 二、QLoRA篇

### 2.1 QLoRA 的思路是怎么样的？
### 2.2 QLoRA 的特点是什么？
## 三、AdaLoRA篇

### 3.1 AdaLoRA 的思路是怎么样的？
## 四、LoRA权重是否可以合入原模型？

## 五、ChatGLM-6B LoRA后的权重多大？

## 六、LoRA 微调优点是什么？

## 七、LoRA微调方法为啥能加速训练？

## 八、如何在已有LoRA模型上继续训练？

## 九、LoRA 缺点是什么？

## 十、LoRA这种微调方法和全参数比起来有什么劣势吗？

# 推理
## 为什么大模型推理时显存涨的那么多还一直占着？
## 大模型在gpu和cpu上推理速度如何？
## 推理速度上，int8和fp16比起来怎么样？
## 大模型有推理能力吗？
## 大模型生成时的参数怎么设置？
## 有哪些省内存的大语言模型训练/微调/推理方法？
### 6.1 如何 估算模型所需的RAM？
### 6.2 Fp16-mixed precision
### 6.3 Int8-bitsandbytes
### 6.4 LoRA
### 6.5 Gradient Checkpointing
### 6.6 Torch FSDP+CPU offload
## 如何让大模型输出合规化
## 应用模式变更

# 预训练
## 为什么要增量预训练？
## 进行 增量预训练 需要做哪些准备工作？
## 增量预训练 所用 训练框架？
## 增量预训练 训练流程 是怎么样？

# 评测
## 大模型怎么评测？
## 大模型的honest原则是如何实现的？模型如何判断回答的知识是训练过的已知的知识，怎么训练这种能力？
## 如何衡量大模型水平？
## 大模型评估方法 有哪些？
## 大模型评估工具 有哪些？

# 强化学习
## 简单介绍强化学习？
## 简单介绍一下 RLHF？
## 奖励模型需要和基础模型一致吗？
## RLHF 在实践过程中存在哪些不足？
## 如何解决 人工产生的偏好数据集成本较高，很难量产问题？
## 如何解决三个阶段的训练（SFT->RM->PPO）过程较长，更新迭代较慢问题？
## 如何解决 PPO 的训练过程同时存在4个模型（2训练，2推理），对计算资源的要求较高 问题？

# 训练集
## SFT（有监督微调）的数据集格式？
## RM（奖励模型）的数据格式？
## PPO（强化学习）的数据格式？
## 找数据集哪里找？
## 微调需要多少条数据？
## 有哪些大模型的训练集？
## 进行领域大模型预训练应用哪些数据集比较好？

# 显存问题
## 大模型大概有多大，模型文件有多大?
## 能否用4 * v100 32G训练vicuna 65b？
## 如果就是想要试试65b模型，但是显存不多怎么办？
## nB模型推理需要多少显存？
## nB模型训练需要多少显存？
## 如何 估算模型所需的RAM？
## 如何评估你的显卡利用率?
## 测试你的显卡利用率 实现细节篇
### 如何查看多机训练时的网速？
### 如何查看服务器上的多卡之间的NVLINK topo？
### 如何查看服务器上显卡的具体型号?
### 如何查看训练时的flops？（也就是每秒的计算量）
### 如何查看对deepspeed的环境配置是否正确？
### tf32格式有多长？
### 哪里看各类显卡算力比较？
### （torch profiler）如何查看自己的训练中通信开销？

# 分布式训练
## 理论篇
### 1.1 训练 大语言模型 存在问题？
### 1.2 什么是 点对点通信？
### 1.3 什么是 集体通信？
### 1.4 什么是 数据并行？
### 1.5 数据并行 如何 提升效率？
### 1.6 什么是 流水线并行？
### 1.7 什么是 张量并行 (intra-layer)？
### 1.8 数据并行 vs 张量并行 vs 流水线并行?
## 实践篇
### 2.1 假如有超多的8卡A100节点（DGX A100），如何应用3D并行策略？
### 2.2 如果想构这样一个大规模并行训练系统，训练框架如何选？
### 2.3 训练框架如何选？
## 并行化策略选择篇
### 3.1 如何选择一款分布式训练框架？
### 3.2 如何选择一款分布式训练框架？
### 3.3 单GPU
### 3.4 单节点多卡
### 3.5 多节点多卡
## 问题篇
### 4.1 推理速度验证
### 4.2 并行化训练加速
### 4.3 deepspeed 训练过程，报找不主机
### 4.4 为什么 多机训练效率不如单机？
### 4.5 多机训练不通，DeepSPeed配置问题

# 分布式训练-流水线并行
## 为什么需要流水线并行（Pipeline Parallelism）？

## 一、流水线并行（Pipeline Parallelism） 优化目标是什么？

## 二、图解 流水线并行（Pipeline Parallelism）模型并行 必要性？

## 三、流水线并行（Pipeline Parallelism） 图解？

## 四、流水线并行（Pipeline Parallelism）优缺点？

# 分布式训练-nn.DataParallel
## 为什么需要nn.DataParallel？

## 一、pytorch中的GPU操作默认是什么样？

## 二、介绍一下 nn.DataParallel 函数？

## 三、nn.DataParallel 函数 处理逻辑 介绍一下？

## 四、nn.DataParallel 函数 常见问题及解答 有哪些？

### 4.1 多GPU计算减少了程序运行的时间？
### 4.2 如何保存和加载多GPU训练模型呢？
### 4.3 为什么第一块卡的显存会占用的更多一些？
### 4.4 直接使用nn.DataParallel的时候，训练采用多卡训练，会出现一个warning？
### 4.5 device_ids 0 被占用问题
## 五、nn.DataParallel 函数 参数更新方式 ？

## 六、nn.DataParallel 函数 优点 介绍一下？

## 七、nn.DataParallel 函数 缺点 介绍一下？

## 八、nn.DataParallel 函数 实战？

# 分布式训练-nn.parallel.DistributedDataparallel
## 为什么需要 nn.parallel.DistributedDataParallel ？

## 一、什么是 DistributedDataParallel 核心 —— Ring-AllReduce？

## 二、nn.parallel.DistributedDataParallel 函数 介绍一下？

## 三、nn.parallel.DistributedDataParallel 函数 如何多卡加速训练？

## 四、nn.parallel.DistributedDataParallel 实现流程介绍一下？

## 五、nn.parallel.DistributedDataParallel 参数更新介绍一下？

## 六、nn.DataParallel(以下简称DP) vs DistributedDataParallel(以下简称DDP)介绍一下？

## 七、DistributedDataParallel(以下简称DDP) 优点有哪些？

## 八、DistributedDataParallel(以下简称DDP) 缺点有哪些？

# 分布式训练-torch.multiprocessing
## 一、torch.multiprocessing 函数介绍一下？

## 二、torch.multiprocessing 函数如何使用？

## 三、介绍一下 共享CUDA张量？

## 四、介绍一下 共享策略？

## 五、torch.multiprocessing 函数使用

# 分布式训练-AMP混合精度训练
## 为什么需要 AMP混合精度训练？

## 一、什么是自动混合精度训练(AMP)

## 二、为什么需要自动混合精度？

## 三、混合精度训练的优点是什么？

## 四、混合精度训练的缺点是什么？

## 五、混合精度训练的关键技术是什么？

## 六、介绍一下 混合精度训练 动态损失缩放？

## 七、如何在PyTorch中使用自动混合精度？

## 八、如何使用 AMP混合精度训练 ？

# 分布式训练-pytorch的deepspeed
## 一、为什么需要 Deepspeed？

## 二、DeepSpeed 基本概念 介绍一下？

## 三、DeepSpeed 通信策略 介绍一下？

## 四、DeepSpeed 如何使用？

## 五、DeepSpeed 代码实现？

## 七、训练精度 介绍一下？

## 八、获取模型参数 介绍一下？

# 分布式训练-accelerate 
## 一、为什么需要 accelerate 分布式训练？

## 二、什么是 accelerate 分布式训练?

## 三、accelerate 分布式训练 原理讲解？

## 四、accelerate 分布式训练 如何实践？

# 分布式训练-ZeRO学习
## 一、什么是 3D 并行？

## 二、3D 并行 策略有哪些？

## 三、为什么需要 ZeRO？

## 四、ZeRO 的 核心思想是什么？

## 五、ZeRO 显存如何分配？

## 六、ZeRO 优化策略是怎么样？

## 七、ZeRO Offload后的计算流程是怎么样？

# agent
## 如何给LLM注入领域知识？
## 如果想要快速体验各种模型，该怎么办？

# Token及模型参数准备
## 预训练数据 Token 重复 是否影响 模型性能？
## SFT需要训练Token数？

# 位置编码
## 1 什么是位置编码？

## 2 什么是绝对位置编码？

## 3 什么是相对位置编码？

## 4 旋转位置编码 RoPE篇

### 4.1 旋转位置编码 RoPE 思路是什么？
### 4.2 推导一下 旋转位置编码 RoPE ？
### 4.3 旋转位置编码 RoPE 有什么优点？
### 4.4 旋转位置编码 RoPE 被哪些 LLMs 应用？
## 5 长度外推问题篇

### 5.1 什么是 长度外推问题？
### 5.2 长度外推问题 的 解决方法 有哪些？
## 6 ALiBi (Attention with Linear Biases)篇

### 6.1 ALiBi (Attention with Linear Biases) 思路是什么？
### 6.2 ALiBi (Attention with Linear Biases) 的偏置矩阵是什么？有什么作用？
### 6.3 ALiBi (Attention with Linear Biases) 有什么优点？
### 6.4 ALiBi (Attention with Linear Biases) 被哪些 LLMs 应用？

# Tokenizer
## Byte-Pair Encoding(BPE)篇

### 1 Byte-Pair Encoding(BPE) 如何构建词典？
## WordPiece 篇

### 1 WordPiece 与 BPE 异同点是什么？
## SentencePiece 篇

### 简单介绍一下 SentencePiece 思路？
## 对比篇

### 1 举例 介绍一下 不同 大模型LLMs 的分词方式？
### 2 介绍一下 不同 大模型LLMs 的分词方式 的区别？

# 让英文llm支持中文-构建中文tokenization
## 一、为什么需要 构建中文tokenization？

## 二、如何对 原始数据预处理？

## 三、如何构建中文的词库？

## 四、如何使用transformers库加载sentencepiece模型？

## 五、如何合并英文词表和中文词表？

## 六、怎么使用修改后的词表？

## 总结一下 构建中文tokenization？

# 让英文llm支持中文-继续预训练
## 一、为什么需要进行继续预训练？

## 二、如何对 继续预训练 数据预处理？

## 三、如何 构建模型？

## 四、如何 使用模型？

# 让英文llm支持中文-指令微调
## 一、为什么需要对预训练模型进行指令微调？

## 二、对预训练模型进行指令微调 数据 如何处理？

## 三、对预训练模型进行指令微调 tokenization 如何构建？

## 四、对预训练模型进行指令微调 模型 如何构建？

## 五、是否可以结合 其他库 使用？

# Layer normalization
## Layer normalization-方法篇

### Layer Norm 篇
#### Layer Norm 的计算公式写一下？
### RMS Norm 篇 （均方根 Norm）
#### RMS Norm 的计算公式写一下？
#### RMS Norm 相比于 Layer Norm 有什么特点？
### Deep Norm 篇
#### Deep Norm 思路？
#### 写一下 Deep Norm 代码实现？
#### Deep Norm 有什么优点？
### Layer normalization-位置篇

#### 1 LN 在 LLMs 中的不同位置 有什么区别么？如果有，能介绍一下区别么？
## Layer normalization 对比篇

### LLMs 各模型分别用了 哪种 Layer normalization？

# 激活函数
## 1 介绍一下 FFN 块 计算公式？

## 2 介绍一下 GeLU 计算公式？

## 3 介绍一下 Swish 计算公式？

## 4 介绍一下 使用 GLU 线性门控单元的 FFN 块 计算公式？

## 5 介绍一下 使用 GeLU 的 GLU 块 计算公式？

## 6 介绍一下 使用 Swish 的 GLU 块 计算公式？

## 各LLMs 都使用哪种激活函数？

# 模型加速
## 当前优化模型最主要技术手段有哪些？
## 推理加速框架有哪一些？都有什么特点？
## 3 vLLM 篇

### 3.1 vLLM 的 功能有哪些？
### 3.2 vLLM 的 优点有哪些？
### 3.3 vLLM 的 缺点有哪些？
### 3.4 vLLM 离线批量推理？
### 3.5 vLLM API Server？
## 4 Text generation inference 篇

### 4.1 介绍一下 Text generation inference？
### 4.2 Text generation inference 的 功能有哪些？
### 4.3 Text generation inference 的 优点有哪些？
### 4.4 Text generation inference 的 缺点有哪些？
### 4.5 Text generation inference 的 使用docker运行web server？

# 部署加速-Pagedattention
## 一、vLLM 用于大模型并行推理加速 存在什么问题？

## 二、vLLM 如何 优化 大模型并行推理加速？

## 三、什么是 PagedAttention？

## 四、 PagedAttention 如何存储 连续的key和value？

## 五、 PagedAttention 技术细节？

## 六、 PagedAttention 如何 实现安全共享？

## 七、 PagedAttention 源码介绍？

# 推理加速工具-VLLM
## 1.2 为什么 需要 vLLM ?
## 1.3 vLLM 具有哪些特点 ?
## 1.4 vLLM 支持哪些 Huggingface 模型 ?
## 二、vLLM 性能如何？

## 三、vLLM 依赖包

## 四、vLLM 如何安装？

## 五、vLLM 如何使用？

## 六、vLLM 分布式推理与服务

# 部署加速-Faster Transformer
## 一、为什么需要 FasterTransformer？

## 二、FasterTransformer 介绍一下？

## 三、FasterTransformer 核心是什么？

## 四、FasterTransformer 优化？

# 高性能推理框架-lightLLM
## 一、引言

### 1.1 前言
### 1.2 为什么 需要 LightLLM ?
### 1.3 目前 LLM推理框架 有 哪些?
## 二、LightLLM 介绍一下？

### 2.1 什么是 LightLLM ？
### 2.2 Token Attention 介绍？
### 2.3 Efficient Router 介绍？
## 三、LightLLM 性能表现 介绍？

## 四、LightLLM 依赖包 有哪些？

## 五、LightLLM 如何安装？

### 5.1 下载 LightLLM
### 5.2 安装 LightLLM 依赖
### 5.3 安装 LightLLM
## 六、LightLLM 如何使用？

### 6.1 启动 LightLLM 服务
## 填坑笔记

### LightLLM 支持模型 LLMs 模型？

# LLM推理技术-StreamingLLM
## 1.1 大型语言模型（LLM）存在什么问题？
## 1.2 StreamingLLM 背景介绍
## 1.3 StreamingLLM 核心问题？
## 1.4 StreamingLLM 存在哪些挑战？
## 1.5 目前主流地增加输入文本长度的方法有哪些？
## 二、StreamingLLM 的思路是什么？

# Attention细节
## 1 传统 Attention 存在哪些问题？

## 2 Attention 优化方向

## 3 Attention 变体有哪些？

## 4 Multi-Query Attention 篇

### 4.1 Multi-head Attention 存在什么问题？
### 4.2 介绍一下 Multi-Query Attention？
### 4.3 对比一下 Multi-head Attention 和 Multi-Query Attention？
### 4.4 Multi-Query Attention 这样做的好处是什么？
### 4.5 有 哪些模型 是 使用 Multi-Query Attention？
## 5 Grouped-query Attention

### 5.1 什么是 Grouped-query Attention？
### 5.2 有哪些大模型使用 Grouped-query Attention？
## 6 FlashAttention 介绍一下

## 7 并行 transformer block 介绍一下？

# 大模型幻觉
## 一、什么是大模型幻觉？

## 二、为什么LLM会产生幻觉？

## 三、为什么需要解决LLM的幻觉问题？

## 四、幻觉一定是有害的吗？

## 五、幻觉有哪些不同类型？

## 六、如何度量幻觉？

## 七、如何缓解LLM幻觉？

### 7.1 通过使用外部知识验证主动检测和减轻幻觉
### 7.2 事实核心采样
### 7.3 SelfCheckGPT
## 八、LLMs什么时候最容易产生幻觉？

## 一、什么是 大模型幻觉问题？

## 二、为什么 会 出现 大模型幻觉问题？

## 三、如何 评估 大模型幻觉问题？

## 四、如何 缓解 大模型幻觉问题？

# LLM对比篇
# 百川智能baichuan7B、13B、53B、baichuan2总结篇
## 一、baichuan-7B篇

### 你了解baichuan-7B解构么？介绍一下？
### baichuan-7B 如何 收集原始数据并 构建 训练数据？
### baichuan-7B 如何 提高 训练稳定性和吞吐？
## 二、baichuan-13B篇

### 相比于 baichuan-7B，baichuan-13B 的 特点体现在哪里？
### 如何 对 baichuan-13B 进行推理和部署？
### 如何 对 baichuan-13B 进行微调？
## 三、baichuan-53B篇

### 3.1 baichuan-53B 相比于 baichuan-7B 和 baichuan-13B 有哪些优势？
### 3.2 baichuan-53B 如何对 预训练数据 做处理？
### 3.3 baichuan-53B 如何进行 搜索增强？
## 四、baichuan2篇

### 4.1 baichuan2 与 其他大模型 对比
## 五、baichuan 数据构建篇

### 5.1 baichuan 进行微调时，领域数据：通用数据配比？

# 思维链篇
## 一、什么是思维链提示？

## 二、思维链提示本质是什么？

## 三、思维链提示 与 标准的提示学习方法有什么不同?

## 四、思维链提示 为什么可以提高语言模型的复杂推理能力?它的优势在哪里?

## 五、思维链提示 适用场景 有 哪些？

## 六、思维链提示 目前还存在哪些不足点？

## 七、思维链提示 对推动语言模型复杂推理能力研究有哪些启发和影响?

## 八、思维链提示 对实现真正的通用人工智能仍面临哪些挑战?

## 九、如何通过增加模型规模来获得语言模型强大的思路链推理能力的?这与模型获得的哪些能力有关?

## 十、你认为可以在哪些其他方面应用“思路链提示”这一思路来提升语言模型的能力?

## 十一、如果需要你对 思维链提示 进行改进，你觉得你会改进哪些地方？

## 十二、思维链提示 未来研究方向？
  
# 思维链变体篇
## 思维链 Chain-of-Thought（COT）：思维链的启蒙

### 什么是 思维链 Chain-of-Thought（COT）？
### 思维链 Chain-of-Thought（COT）是思路是什么？
### 思维链 Chain-of-Thought（COT）存在问题？
## 思维树 Tree of Thoughts（TOT）：一种用树结构解决复杂问题的方法

### 为什么需要 思维树 Tree of Thoughts（TOT）？
### 什么是 思维树 Tree of Thoughts（TOT）？
### 思维树 Tree of Thoughts（TOT）涉及问题有哪些？
## 思维图 Graph of Thoughts（GOT）：一种把思维链过程建模层图结构的方法

### 为什么 需要 思维图 Graph of Thoughts（GOT）？
### 什么是 思维图 Graph of Thoughts（GOT） ？
### 思维图 Graph of Thoughts（GOT）核心思想是什么 ？
## 思维算法 Algorithm of Thoughts（AOT）：一种用DFS/BFS示例解决问题的方法

### 为什么 需要 思维算法 Algorithm of Thoughts（AOT）？
### 思维算法 Algorithm of Thoughts（AOT）思路是什么？
### 思维算法 Algorithm of Thoughts（AOT） vs 其他 COT 的 区别？
## 思维链 Chain-of-Thought（COT） 有哪些 应用场景？

### 思维链 Chain-of-Thought（COT） 有哪些 局限性？

# RAG

# 大模型生成去重
## 一、什么是生成式大模型？

## 二、大模型是怎么让生成的文本丰富而不单调的呢？

## 三、生成式大模型 存在哪些问题？

## 四、生成式大模型 为什么会出现 重复生成现象？

## 五、生成式大模型 有哪些解决方法？

### 5.1 Unlikelihood Training
### 5.2 Repetition Penalty
### 5.3 Contrastive Search
### 5.4 Beam Search
### 5.5 TopK sampling
### 5.6 Nucleus sampler
### 5.7 Temperature
### 5.8 No repeat ngram size
### 5.9 重复率指标检测
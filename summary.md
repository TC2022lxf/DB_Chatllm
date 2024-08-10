# 2024.8.2
## 自我介绍
1. 介绍个人信息，姓名、学校、专业、年级，在校获奖如蓝桥杯、robcon、算法比赛、挑战杯等以及
每年的奖学金，成绩专业前三，在校项目做过unet医学分割、yolo物体检测、结合llm识别图片
等，并申请软著撰写论文，也有成功申请校级省级等项目基金。
24年1月至24年7月在广州晨扬通信公司实习，岗位是大模型算法工程师实习，指导老师是浙大张教
授。做的大项目是AI数字人，涉及化妆品、电信、政务等多个方面，应用如微信聊天机器人、电话
视频销售、线下店机器人导购、构建不同人格的AI实体。我主要是负
责数字人的问答，包括但不限于前期的数据收集数据清晰和数据结构设计、lora微调开源大模型
qwen2:72b、基于ollama推理框架和langchain框架构建工程代码、设计RAG方案提高llm在垂直领
域的回答质量、设计agent和tool实现AI数字人的多项功能如订单查询、产品图片、支付链接等等。
更加主要的还是对语言模型的回答准确性的负责
## lora的数据格式
1. 采用的是指令微调，数据格式是由instruction,input,output组成的字典，其中instruction是用户指令，告知模型其需要完成的任务。input是用户输入，是完成用户指令所必须的输入内容。output是模型应该给出的输出。我们的核心训练目标是让模型具有理解并遵循用户指令的能力。训练时数据格式化成input_ids,attention_mask,labels,其中input_ids包含instruction、input、output。attetntion_mask全一，至于为什么不用因果注意力掩码呢我觉得根据lora训练的目标有关，目标通常是调整和优化参数，使模型在整个输入序列上的表现更好。这与生成任务中的逐步生成过程不同。还有就是label，与input_ids一样，表明输入序列和输出序列都参与损失计算，如果输入序列*-100则表示输入序列不参与损失计算，-100在transformers库通常表示忽略这些位置的损失计算。

## lora代码如何来
1. lora代码是使用github上的羊驼lora代码，集成微调工具使用的是llama-factory，可以进行（增量）预训练、（多模态）指令监督微调、奖励模型训练、PPO 训练、DPO 训练、KTO 训练、ORPO 训练等等。


## 数据如何清洗
采用基于规则的清洗方法，划分为过滤类规则和清洗类规则两大类。

其中，命中过滤规则的数据项将被弃用，而清洗规则旨在处理并保留所需的数据。

1）过滤类-敏感词规则：基于积累的敏感词库，清洗丢弃涉政、涉黄、涉暴、涉恐等数据项；

2）过滤类-无效输入输出：此类规则主要针对 将各类文档转换成文本数据缺陷进行专项清理，丢弃一些无效的数据项；无效输入如"<一段文本>"，无效输出如"[图画]"；

3）清洗类-关键词规则：根据整理的关键词/正则列表进行数据的替换，包括：清理特殊标志位字符、清理非可见字符、清理标签、繁简转换等；

4）清洗类-特殊逻辑规则：此类规则用于清洗一些特殊现象数据，如指令与输入重复等。

当然我们可以用开源的项目，在上面修改，这样就不用从零开始写了。如omniparse
## lora微调的流程
- 指令集构建，格式通常为instruction、input、output
- 数据格式化，数据格式通常为input_ids、attention_mask、labels
- 加载tokenizer和模型
- 定义loraconfig，主要的参数是秩、缩放参数lora_alpha(保持不同r下的权重变化稳定性)、target_modules即lora应用的模块(通常是attention层或者一些线性层)、lora_dropout丢失概率(丢失部分神经元来减少过拟合)、Lora bias偏差类型、task_type微调的任务类型(如casual_llm,seq_cls,question_ans)
- 定义trainingArguments，开始训练，保存lora权重，加载lora权重推理，或者合并权重
## 介绍一下多轮对话
1. 多轮对话是指uer和assistance通过多次交流来达成共识或完成某项任务的过程。多轮对话技术相对于单轮对话，需要考虑上下文信息、用户输入和模型输出的更复杂交互，需要模型具备更高的上下文理解和推理能力。可以通过微调来适应不同的对话任务和环境。

## 多轮对话如何微调。
1. 还是用lora微调，但是在处理数据格式上要修改一下，借鉴了github开源项目firefly，数据格式可以是instruction、category、conversation，其中instruction指引模型进行对话的任务，category指对话场景的类别，conversation是user和assistance的对话。数据格式化也是按照原本的lora代码，即input_dis\attention_mask\labels，input_ids包含instruction、category和conversation，其中conversation被处理成对应的user和assistance格式。attention_mask依旧全一、labels则只对assistance的对话进行损失计算，而其他都*-100即忽略损失计算。
## 算法题：二维DP、二分

两个字符串x和y，长度分别是n和m，n和m不一定相等，有三种操作，增加字符、减少字符、替换字符。问x变成y的最少操作是多少，例子x=aabb,y=abc则需要2个操作，x[1]删除得到abb，x[2]替换成c得到abc


``` python
s1 = "aabb"
s2 = "abc"
n = len(s1)
m = len(s2)
dp = [[0]*(m+1) for i in range(n+1)]

for i in range(n+1):
    dp[i][0] = i
for j in range(m+1):
    dp[0][j] = j

for i in range(1,n+1):
    for j in range(1,m+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1]
        else:
            dp[i][j]=min(dp[i-1][j]+1,dp[i-1][j-1]+1,dp[i][j-1]+1)
print(dp[n][m])

```
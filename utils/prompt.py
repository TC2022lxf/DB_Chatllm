from langchain_core.prompts import PromptTemplate


def create_prompt_template():
    prompt_template = """
            我将给你一个知识文本context,以及一个与你的工作有关的问题question.
            如果你在context中无法搜寻到问题的答案,即使你本身知道答案但我也请你不要回答,只需要告诉我你不知道答案就行.
            知识文本为:{context},
            问题为:{question}.
            """
    prompt_template1 = """Question: {question}
    
    Answer: """
    prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
    return prompt

def create_prompt_template_no_context():
    prompt_template1 = """Question: {question}

        Answer: """
    prompt = PromptTemplate(template=prompt_template1, input_variables=["question"])
    return prompt
from langchain_core.prompts import PromptTemplate


def create_prompt_template():
    prompt_template = """
            我将给你一个知识文本context,以及一个与你的工作有关的问题question.
            如果你在context中无法搜寻到问题的答案,即使你本身知道答案但我也请你不要回答,只需要告诉我你不知道答案就行.
            知识文本为:{context},
            问题为:{question}.
            """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context","question"])
    return prompt

def create_prompt_template_no_context():
    prompt_template1 = """问题: {question}

        答案: """
    prompt = PromptTemplate(template=prompt_template1, input_variables=["question"])
    return prompt

def prompt1():

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer in Chinese:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return PROMPT

def prompt2():
    question_prompt_template = """
    {context}
    Question: {question}
    """
    QUESTION_PROMPT = PromptTemplate(
        template=question_prompt_template, input_variables=["context", "question"]
    )

    combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer Chinese. 
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    It's important to keep answers to 500 words or less
    QUESTION: {question}
    =========
    {summaries}
    =========
    Answer in Chinese:"""
    COMBINE_PROMPT = PromptTemplate(
        template=combine_prompt_template, input_variables=["summaries", "question"]
    )
    return QUESTION_PROMPT,COMBINE_PROMPT

def prompt3():
    refine_prompt_template = (
        "The original question is as follows: {question}\n"
        "We have provided an existing answer: {existing_answer}\n"
        "We have the opportunity to refine the existing answer"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{context_str}\n"
        "------------\n"
        "Given the new context, refine the original answer to better "
        "answer the question. "
        "If the context isn't useful, return the original answer. Reply in Chinese."
    )
    refine_prompt = PromptTemplate(
        input_variables=["question", "existing_answer", "context_str"],
        template=refine_prompt_template,
    )

    initial_qa_template = (
        "Context information is below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the question: {question}\nYour answer should be in Chinese.\n"
    )
    initial_qa_prompt = PromptTemplate(
        input_variables=["context_str", "question"], template=initial_qa_template
    )
    return refine_prompt,initial_qa_prompt

def prompt4():
    from langchain.output_parsers import RegexParser

    output_parser = RegexParser(
        regex=r"(.*?)\nScore: (.*)",
        output_keys=["answer", "score"],
    )

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    In addition to giving an answer, also return a score of how fully it answered the user's question. This should be in the following format:

    Question: [question here]
    Helpful Answer In Chinese: [answer here]
    Score: [score between 0 and 100]

    Begin!

    Context:
    ---------
    {context}
    ---------
    Question: {question}
    Helpful Answer In Chinese:"""
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
        output_parser=output_parser,
    )
    return PROMPT

def prompt5():
    question_prompt_template = """Use the following portion of a long document to see if any of the text is relevant to answer the question. 
        Return any relevant text in Chinese.
        {context}
        Question: {question}
        Relevant text, if any, in Chinese:"""
    QUESTION_PROMPT = PromptTemplate(
        template=question_prompt_template, input_variables=["context", "question"]
    )
    template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCE").
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.

        Respond in Chinese.

        QUESTION: {question}
        =========
        {summaries}
        =========
        FINAL ANSWER IN Chinese:"""
    COMBINE_PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
    return QUESTION_PROMPT,COMBINE_PROMPT
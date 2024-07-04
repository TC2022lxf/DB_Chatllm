"""
层次结构，v2版本
json结构
[
    {
        "parent_title": 父标题,
        "title": 标题,
        "level": 层级,
        "unique_id": 唯一标识,
        "parent_id": 父标识,
        "content": ""
        "children": [{"嵌套sub标题"}]
    }
]

"""
try:
    from utils.llm import *
except ModuleNotFoundError as e:
    import sys

    sys.path.append('D:\project\pythonProject')
    from utils.llm import *

    print(f"Warning: {e}. The 'env' module could not be found, continuing without it.")

import json


def parse_md_to_json(md_list):
    md_list = [item for item in md_list if item.strip()]  # 去除空行
    json_data = {  # 创建当前标题节点
        "parent_title": None,
        "title": None,
        "level": None,
        "unique_id": None,
        "parent_id": None,
        "content": "",
        "children": [],
    }
    stack = [{"level": 0, "title": None, "unique_id": None, "node": json_data}]

    for item in md_list:
        if item.startswith("#"):
            level = item.count("#")
            title = item[level:].strip()
            unique_id = str(uuid.uuid4())

            while stack and stack[-1]["level"] >= level:  # 弹出堆栈中级别高于或等于当前标题级别的元素，确保堆栈顶部是当前标题的父节点。
                stack.pop()

            current_node = {  # 创建当前标题节点
                "parent_title": stack[-1]["title"] if stack else None,
                "title": title,
                "level": level,
                "unique_id": unique_id,
                "parent_id": stack[-1]["unique_id"] if stack else None,
                "content": "",
                "children": [],
            }
            stack[-1]["node"]["children"].append(current_node)  # 将当前标题节点添加到父节点的子节点列表中（递归核心）
            stack.append({"level": level, "title": title, "unique_id": unique_id, "node": current_node})

        else:
            stack[-1]["node"]["content"] += str(item) + "\n"
    return json_data


def llm_summary(content_str):
    message = [SystemMessage(
        content="You are a summary model. You will receive a paragraph of text. If the text is too redundant, provide a concise summary; otherwise, no summary will be made. Remember not to modify the meaning of the original text, you will return the abstract in markup format.")]
    message.append(HumanMessage(content=content_str))
    response = llm.invoke(message)
    response = "summary:" + response
    logger.info(response)
    return response


def summarize_node(node):
    # 递归遍历节点
    for dc in node:
        if dc["children"] is not None:
            # 递归处理子节点
            summarize_node(dc["children"])
            # 子节点的摘要内容
            child_summaries = ""
            for dict in dc["children"]:
                child_summaries += '\n' + (dict['content'])

            if child_summaries:
                # 获取当前节点内容
                if not dc['content']:
                    dc['content'] = '\n' + (llm_summary(child_summaries))
                else:
                    combined_content = dc['content'] + llm_summary(child_summaries)
                    dc['content'] = '\n' + (llm_summary(combined_content))
    return node


def process_json(json_data):
    # 遍历一级标题
    for key, value in json_data.items():
        if key == "content" and value is not None:
            summarize_node(value)

    return json_data


def merge_paragraphs(input_text):
    paragraphs = input_text.split('\n')
    merged_paragraphs = []
    current_paragraph = ""

    for paragraph in paragraphs:
        if len(current_paragraph) + len(paragraph) < 50:
            # 如果当前段落和新段落长度小于50，则合并
            if current_paragraph:
                current_paragraph += '\n' + paragraph
            else:
                current_paragraph = paragraph
        else:
            # 如果当前段落长度大于等于50，则添加当前段落到列表，并重置当前段落
            if current_paragraph:
                merged_paragraphs.append(current_paragraph)
            current_paragraph = paragraph

    # 添加最后一个段落
    if current_paragraph:
        merged_paragraphs.append(current_paragraph)

    return merged_paragraphs


def cut_content(json_data, max_length=1000):
    for title, content in json_data.items():
        if isinstance(content, dict):
            # 递归处理子节点
            cut_content(content, max_length)
            content['content'] = merge_paragraphs(content['content'])


def summary_md(md_path):
    with open(md_path, "r") as f:
        md_text = f.read()
    md_text_list = md_text.split("\n")
    json_output = summarize_node([parse_md_to_json(md_text_list)])
    with open(f'{md_path[:-3]}.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    import uuid

    md_path = 'knowledge_data/23903-i00.md'
    summary_md(md_path)

    # json_path='knowledge_data/23122-i10.json'
    # with open(json_path, 'r', encoding='utf-8') as f:
    #     json_output = json.load(f)
    # cut_content(json_output)
    # with open(f'{json_path[:-3]}_cut.json', 'w', encoding='utf-8') as f:
    #     json.dump(json_output, f, ensure_ascii=False, indent=4)

from flask import Flask, jsonify, request

app = Flask(__name__)

from utils.llm import load_llm
llms = load_llm()
def llm(question):

    # 假设你已经有了实现的逻辑，例如调用LLM模型来获取答案
    answer = "答案：{}".format(llms.invoke(question))  # 这里仅作演示，实际应替换为你的模型调用逻辑
    return answer


@app.route('/api/answer', methods=['POST']) # 方法设置成post
def get_answer():
    data = request.get_json() # 接收json格式的数据
    if 'question' not in data:
        return jsonify({"error": "请求缺少question参数"}), 400

    question = data['question']
    answer = llm(question)

    return jsonify({"answer": answer}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
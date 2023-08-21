from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from chatbot import get_response, predict_class

app = Flask(__name__)

CORS(app)

@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    username=request.get_json().get("username")
    predict = predict_class(text)
    intents = json.loads(open("int.json", encoding='utf-8').read())
    response = get_response(predict,intents,username)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)

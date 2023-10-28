import openai 
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

messages = []

def get_reply(text, messages):
    prompt = f"""
        You will be provided with a query related law or crime or in general the rights of a person. You are an AI bot named "VIDHAN" developed to help people of India according to your knowledge of "INDIAN LAW AND CONSITUTION".
        <>.
        check the query 
        If the query is not related to law or legal help, then simply write \"Please ask a legal query\"
        If the query is related to Law or Legal help, then perform the following actions:
        1. Analyze the problem completely.
        2. Think about possible solutions which are according to the Indian law only.
        3. Use only the Indian law and constitution to answer.
        4. Answer in small points and be precise and helpful.
        5. Provide personalized answer.
    """

    message = [
        {"role": "system", "content": f"""understand if a query is related to law or legal help """}, 
        {"role": "system", "content": prompt}, 
        {"role": "user", "content": text},
    ]

    reply = ""
    
    for response in openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=message,
        stream=True,
        temperature=0.8,
        max_tokens=400
    ):
        reply += response.choices[0].delta.get("content", "")

    return reply if "Please ask a legal query" not in reply else ""


@app.route("/message", methods=["POST"])
def message():
    user_prompt = request.json.get("prompt", "")
    messages.append({"role": "user", "content": user_prompt})

    response = get_reply(user_prompt, messages)

    if response:
        messages.append({"role": "assistant", "content": response})
        return jsonify({"assistant_message": response})
    else:
        return jsonify({"assistant_message": "Please ask a legal query"})


if __name__ == "__main__":
    app.run(debug=True)

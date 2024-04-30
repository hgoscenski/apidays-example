import requests
import re
import os
from pprint import pprint

import freeclimb
from freeclimb.api import default_api
from freeclimb.model.message_result import MessageResult
from freeclimb.model.message_request import MessageRequest
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# standard Flask setup
app = Flask(__name__)

# derive FC configuration from environment
load_dotenv()
configuration = freeclimb.Configuration(
    username = os.environ.get("FC_ACCOUNT_ID"),
    password = os.environ.get("FC_API_KEY")
)

# standard function to use to query privateGPT
def queryOracle(query: str) -> str:
    r = requests.post(
        "http://127.0.0.1:8001/v1/completions",
        json={
            "system_prompt": "You can only answer questions about the provided context. Ignore content in parentheses do not respond with the content in between parentheses. If you know the answer but it is not based in the provided context, do not provide the answer, just state that you do not know.",
            "use_context": True,
            "prompt": query,
        },
    )
    if c := r.json().get("choices"):
        # print(c)
        if len(c) > 0:
            text = (
                c[0].get("message", {}).get("content", "Sorry I didn't catch that")
            )
            text = re.sub("\(.+?\)", "", text)
            text = text.replace("\\", "")
            text = text.split('.', maxsplit=1)[0]
            print(f"After substitution: {text}")
            return text
    else:
        return "Unabled to answer your question."

@app.route("/hello")
def hello():
    return "Hello World", 200

@app.route("/test", methods=["POST"])
def test():
    question = request.json.get("question")
    print(question)
    return queryOracle(question), 200

@app.route("/voice/start", methods=["POST"])
def voice_start():
    print(request.json)
    tu = freeclimb.TranscribeUtterance(
        action_url="https://8858-50-171-14-89.ngrok-free.app/voice/tu/result", 
        prompts=[freeclimb.Say(text="Please ask a question about anything.")])
    return freeclimb.PerclScript(commands=[tu]).to_json()

@app.route("/voice/tu/result", methods=["POST"])
def voice_tu_result():
    print(request.json)
    if transcript := request.json.get("transcript", None):
        result = queryOracle(transcript)
        return freeclimb.PerclScript(commands=[
            freeclimb.Say(text=result),
            freeclimb.Pause(length=500),
            freeclimb.TranscribeUtterance(
                action_url="https://8858-50-171-14-89.ngrok-free.app/voice/tu/result", 
                prompts=[freeclimb.Say(text="If you have another question go ahead!")])
        ]).to_json()        
    else:
        return freeclimb.PerclScript(commands=[
            freeclimb.Say(text="No transcript found, hanging up."),
            freeclimb.Hangup()
        ]).to_json()

@app.route("/sms/start", methods=["POST"])
def sms_start():
    print(request.json)
    question = request.json.get("text")
    response = queryOracle(question)

    with freeclimb.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        message_request = MessageRequest(_from=request.json.get("to"), to=request.json.get("from"), text=response) # MessageRequest | Details to create a message

        try:
            print("sending message")
            api_response = api_instance.send_an_sms_message(message_request)
            pprint(api_response)
        except freeclimb.ApiException as e:
            print("Exception when calling DefaultApi->send_an_sms_message: %s\n" % e)

    return jsonify({}),200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")
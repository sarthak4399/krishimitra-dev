from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    if 'hello' in incoming_msg:
        msg.body('Hi, I am a chatbot. You can ask me anything.')
    elif 'bye' in incoming_msg:
        msg.body('Bye, see you soon.')
    else:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Q: {incoming_msg}\nA:",
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["\n", " Q:", " A:"]
        )
        msg.body(response['choices'][0]['text'])
    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

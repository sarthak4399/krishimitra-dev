from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'KMFAMILY'  # Replace with your actual verification token
PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBO5yhFLipIUzNDCbKBrddxGgWqpc3EkEYGa7L5d4D1jYZAUu4j888j96HjBfhjsA3KBfelZAYZCaZATY5C4ecFmUbgNZAMnlFaZB7FR5h0vczdVWn2bNuFA2zXoxHfqsXwhENhrb3ZBDMUpFDAOfraK1BIVnyZBAaUUZBm7W1YPMVNYGKpdi1yZBtvhrMmpuilGgZC8HygL0EonVlZBKsHgvHaJXEZCmRF'


@app.route('/')
def index():
    return "Hello"


def register_user():

    pass


def send_msg(msg):
    headers = {
        'Authorization': 'Bearer EAAJztZAX6JRwBO5yhFLipIUzNDCbKBrddxGgWqpc3EkEYGa7L5d4D1jYZAUu4j888j96HjBfhjsA3KBfelZAYZCaZATY5C4ecFmUbgNZAMnlFaZB7FR5h0vczdVWn2bNuFA2zXoxHfqsXwhENhrb3ZBDMUpFDAOfraK1BIVnyZBAaUUZBm7W1YPMVNYGKpdi1yZBtvhrMmpuilGgZC8HygL0EonVlZBKsHgvHaJXEZCmRF',
    }
    json_data = {
        'messaging_product': 'whatsapp',
        'to': ' 9196046 17753',
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post(
        'https://graph.facebook.com/v13.0/135179146337629/messages', headers=headers, json=json_data)
    print(response.text)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    res = request.get_json()
    try:
        if 'entry' in res and res['entry']:
            changes = res['entry'][0].get('changes', [])
            if changes:
                message_value = changes[0].get('value', {})
                if message_value:
                    messages = message_value.get('messages', [])
                    print("Messages", messages)
                    if messages:
                        message_body = messages[0]['text']['body'].lower() if messages and messages[0].get(
                            'text') and 'body' in messages[0]['text'] else None
                        print("Message Body:", message_body)
                        print("Type of message_body:", type(message_body))
                        if message_body == 'hi':
                            send_msg(
                                'Welcome! Please select a language: English, Hindi, Marathi.')

    except Exception as e:
        print(f"Error: {e}")
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

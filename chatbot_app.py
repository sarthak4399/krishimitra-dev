from flask import Flask, request, jsonify
import requests
import os


app = Flask(__name__)

VERIFY_TOKEN = 'KMFAMILY'

PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBOZBG4GU1i8ux73VgL9ZBeorL1NmGu2yzVwIUDc1gH1pr5TMcP6qHuqnPajMXjAAcK19ewiLku9Sa5nuu7i35En2VvaonSAOEMuLmj3DzbaBB7ts0a62fJg0QUKbjDDHZBCuDpPrKGQZAcAqbcxPO2xmTyJNYG7r6IFCiWMHlSQcEldAWSMI5SEo36ZANpVfvRhatJ0748VGNVZAfP1A1wPLx4ZD'
user_preferences = {}
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


@app.route('/')
def index():
    return "Hello"


def validate_user(wa_id):
    registered_user = ['+919403929599', '+917887980143',
                       '+919370708497', '+918446901953', '+918291798609', '+918177834839']
    phn = "+"+wa_id
    if phn in registered_user:
        return wa_id
    else:
        return None


def send_msg(msg, phn):
    headers = {
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    json_data = {
        'messaging_product': 'whatsapp',

        'to': phn,
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post(
        'https://graph.facebook.com/v13.0/135179146337629/messages', headers=headers, json=json_data)


def handle_language_selection(message_body, wa_id):
    if message_body in ['1', '2', '3']:
        language_options = ['English', 'Hindi', 'Marathi']
        selected_language = language_options[int(message_body) - 1]
        user_preferences[wa_id] = {'language_selected': selected_language}
        send_msg(
            f'You have selected {selected_language}. Now, please select a role: 1. Farmer, 2. Dealer', wa_id)
    elif message_body == 'hi':
        send_msg(
            'Welcome! Please select a language: 1. English, 2. Hindi, 3. Marathi.', wa_id)
    else:
        send_msg(
            'Sorry, I did not understand your message. Please select a valid option.', wa_id)


def genrate_media_url(media_id):
    print("Media ID:", media_id)
    headers = {
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    responce = requests.get(
        f'https://graph.facebook.com/v13.0/{media_id}?phone_number_id=135179146337629', headers=headers)
    media_url = responce.json()['url']
    get_image(media_url)
    return media_url


def get_image(media_url):
    headers = {
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    response = requests.get(media_url, headers=headers)
    if response.status_code == 200:
        content_type = response.headers.get('content-type')
        file_extension = content_type.split('/')[-1]
        file_path = f'image.{file_extension}'
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded and saved to: {file_path}")
        # upload_image(response.content)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def upload_image(content):
    response = requests.post(
        f'/upload', files={'photo': content})
    print(response.json())
    pass


def handle_role_selection(message_body, wa_id):
    if message_body in ['1', '2']:
        roles = ['Farmer', 'Dealer']
        selected_role = roles[int(message_body) - 1]
        user_preferences[wa_id] = {'role_selected': selected_role}
        send_msg(
            'Please upload your Aadhar Card and Satbara pdf.' if selected_role == 'Farmer' else
            'Please upload your License number and Aadhar details.', wa_id)
        # upload_image()
    else:
        send_msg('Sorry, I did not understand your role selection. Please select a valid option: 1. Farmer, 2. Dealer', wa_id)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return 'Invalid verification token'
    elif request.method == 'POST':
        res = request.get_json()
        try:
            if 'entry' in res and res['entry']:
                changes = res['entry'][0].get('changes', [])
                if changes:
                    message_value = changes[0].get('value', {})
                    print("Message Value:", message_value)
                    if 'messages' in message_value:
                        for message in message_value['messages']:
                            if 'image' in message:
                                media_id = message['image']['id']
                                contacts = message_value.get('contacts', [])
                                if media_id is not None and contacts:
                                    genrate_media_url(media_id)
                                    send_msg("Image uploaded successfully ✅\nPlease wait while we process your documents.\nSee you shortly! ⏳",
                                             contacts[0].get('wa_id'))
                            elif 'text' in message:
                                contacts = message_value.get('contacts', [])
                                if contacts:
                                    wa_id = contacts[0].get('wa_id')
                                    phn = "+" + validate_user(wa_id)
                                    if not wa_id:
                                        return jsonify({'status': 'error', 'message': 'wa_id not found'})
                                    message_body = message['text']['body'].lower(
                                    )
                                    print("Text Message Body:", message_body)
                                    # Add your logic for handling text messages
                                    if 'language_selected' not in user_preferences.get(wa_id, {}):
                                        handle_language_selection(
                                            message_body, wa_id)
                                    elif 'role_selected' not in user_preferences.get(wa_id, {}):
                                        handle_role_selection(
                                            message_body, wa_id)
                            else:
                                print("Unsupported message type")

        except Exception as e:
            print(f"Error: {e}")
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

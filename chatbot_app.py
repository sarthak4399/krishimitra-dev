from flask import Flask, request, jsonify
import requests
import os
import logging


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

VERIFY_TOKEN = 'KMFAMILY'

PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBO1LkB3ZCSQ5DWfQLUvvUxTRWbSLxf9sPmVoIE4LbsZBZBiTaVsGb6Il05p2X4aOAPa1GqGE44uYJhe6sYRCFXbXxkXs1ScUNxXBz8zU4l74iBjr783VXI3qVdZCne6rJ3n45zReFjAyZAILbXDZBIA3UZCbyolXXiq9kTG4O9BiPwhUGeqg3ugTbtxvZAhQ1h8lqTHjiAj9uptXZCHUyoGVTkPxQZD'
user_preferences = {}
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
messages = {
    'en': {
        'welcome': 'Welcome! Please select a language: 1. English, 2. Hindi, 3. Marathi.',
        'invalid_option': 'Sorry, I did not understand your message. Please select a valid option.',
        'role_selection': 'Please select a role: 1. Farmer, 2. Dealer',
        'upload_documents_farmer': 'Please upload your Aadhar Card and Satbara pdf for farming.',
        'upload_documents_dealer': 'Please upload your License number and Aadhar details for dealership.',
        'documents_uploaded_farmer': 'Thank you for uploading your documents. We will get back to you shortly.',
        'documents_uploaded_dealer': 'Thank you for uploading your documents. We will get back to you shortly.',
        'documents_uploaded': 'Thank you for uploading your documents. We will get back to you shortly.',
        'document_validation_failed': 'Sorry, we could not validate your documents. Please try again.',
    },
    'hi': {
        'welcome': 'स्वागत है! कृपया भाषा का चयन करें: 1. इंग्लिश, 2. हिंदी, 3. मराठी।',
        'invalid_option': 'क्षमा करें, मैंने आपके संदेश को समझा नहीं। कृपया एक वैध विकल्प चुनें।',
        'role_selection': 'कृपया एक भूमिका का चयन करें: 1. किसान, 2. डीलर',
        'upload_documents_farmer': 'कृपया खेती के लिए अपना आधार कार्ड और सतबारा पीडीएफ अपलोड करें।',
        'upload_documents_dealer': 'कृपया डीलरशिप के लिए अपना लाइसेंस नंबर और आधार विवरण अपलोड करें।',
        'documents_uploaded_farmer': 'अपने दस्तावेज़ अपलोड करने के लिए धन्यवाद। हम जल्द ही आपसे संपर्क करेंगे।',
        'documents_uploaded_dealer': 'अपने दस्तावेज़ अपलोड करने के लिए धन्यवाद। हम जल्द ही आपसे संपर्क करेंगे।',
        'documents_uploaded': 'अपने दस्तावेज़ अपलोड करने के लिए धन्यवाद। हम जल्द ही आपसे संपर्क करेंगे।',
    },
    'mr': {
        'welcome': 'स्वागत आहे! कृपया भाषा निवडा: 1. इंग्लिश, 2. हिंदी, 3. मराठी.',
        'invalid_option': 'माफ करा, मला तुमचा संदेश समजला नाही. कृपया एक वैध पर्याय निवडा.',
        'role_selection': 'कृपया एक भूमिका निवडा: 1. शेतकरी, 2. डीलर',
        'upload_documents_farmer': 'कृपया कृषिक्षेत्रात आपला आधार कार्ड आणि सातबारा पीडीएफ अपलोड करा।',
        'upload_documents_dealer': 'कृपया व्यापारीक्षेत्रात आपला लायसेंस नंबर आणि आधार विवरण अपलोड करा।',
        'documents_uploaded_farmer': 'आपले दस्तावेज अपलोड करण्याबद्दल धन्यवाद. आम्ही लवकरच आपल्याशी संपर्क साधू.',
        'documents_uploaded_dealer': 'आपले दस्तावेज अपलोड करण्याबद्दल धन्यवाद. आम्ही लवकरच आपल्याशी संपर्क साधू.',
        'documents_uploaded': 'आपले दस्तावेज अपलोड करण्याबद्दल धन्यवाद. आम्ही लवकरच आपल्याशी संपर्क साधू.',
    },
}


MESSAGE_WELCOME = 'welcome'
MESSAGE_INVALID_OPTION = 'invalid_option'
MESSAGE_ROLE_SELECTION = 'role_selection'
MESSAGE_UPLOAD_DOCUMENTS = 'upload_documents'


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


def send_msg(msg_key, wa_id, language):
    msg = messages.get(language, {}).get(
        msg_key, 'Invalid message key')

    headers = {
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    json_data = {
        'messaging_product': 'whatsapp',
        'to': wa_id,
        'type': 'text',
        "text": {"body": msg}
    }
    response = requests.post(
        'https://graph.facebook.com/v13.0/135179146337629/messages', headers=headers, json=json_data)

    if response.status_code == 200:
        logging.info(f'Message sent successfully: {msg_key} to {wa_id}')


def handle_language_selection(message_body, wa_id):
    if message_body in ['1', '2', '3']:
        language_options = ['en', 'hi', 'mr']
        selected_language = language_options[int(message_body) - 1]
        user_preferences[wa_id] = {'language_selected': selected_language}
        userlang = user_preferences.get(wa_id, {}).get('language_selected')
        print(user_preferences)
        send_msg(MESSAGE_ROLE_SELECTION, wa_id, userlang)
    elif message_body == 'hi':
        send_msg(MESSAGE_WELCOME, wa_id, 'en')


def genrate_media_url(media_id):
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
        # print(f"Image downloaded and saved to: {file_path}")
        upload_image(file_path)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def upload_image(content):
    files = {'photo': open(content, 'rb')}
    response = requests.post(
        'http://192.168.11.120:60000/upload', files=files)
    if response.status_code == 200:
        # print(response.json())
        public_url = response.json()['public_url']
        print(public_url)
        print(f"Image uploaded successfully. Public URL: {public_url}")
        extract_data(public_url)
        print(extract_data(public_url))
    else:
        print(
            f"Failed to upload image. Status code: {response.status_code}, Error: {response.text}")


def extract_data(pub_url):
    data = {'file_url': pub_url}
    response = requests.post('http://192.168.11.120:60001/extract', json=data)
    if response.status_code == 200:
        save_user_data(response.content)
        return response.json()
    else:
        print(
            f"Failed to extract data. Status code: {response.status_code}, Error: {response.text}")
        return None


def save_user_data(data):
    print(data)


def handle_role_selection(message_body, wa_id):
    if message_body in ['1', '2']:
        roles = ['Farmer', 'Dealer']
        selected_role = roles[int(message_body) - 1]
        user_preferences.setdefault(wa_id, {})
        user_preferences[wa_id]['role_selected'] = selected_role
        user_preferences[wa_id]['documents_uploaded'] = False
        selected_language = user_preferences.get(
            wa_id, {}).get('language_selected', 'en')

        msg_key = MESSAGE_INVALID_OPTION
        if selected_role in ['Farmer', 'Dealer']:
            msg_key = MESSAGE_UPLOAD_DOCUMENTS + f'_{selected_role.lower()}'
        send_msg(msg_key, wa_id, selected_language)
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id)


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
                    # print("Message Value:", message_value)

                    if 'messages' in message_value:
                        for message in message_value['messages']:
                            if 'image' in message:
                                media_id = message['image']['id']
                                contacts = message_value.get('contacts', [])
                                if media_id is not None and contacts:
                                    genrate_media_url(media_id)
                                    send_msg(MESSAGE_UPLOAD_DOCUMENTS,
                                             contacts[0].get('wa_id'), 'en')
                            elif 'text' in message:
                                contacts = message_value.get('contacts', [])
                                if contacts:
                                    wa_id = contacts[0].get('wa_id')
                                    phn = "+" + validate_user(wa_id)
                                    if not wa_id:
                                        return jsonify({'status': 'error', 'message': 'wa_id not found'})
                                    message_body = message['text']['body'].lower(
                                    )
                                    # print("Text Message Body:", message_body)
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

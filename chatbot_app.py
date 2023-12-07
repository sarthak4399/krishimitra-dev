from flask import Flask, request, jsonify
import requests
import os


app = Flask(__name__)

VERIFY_TOKEN = 'KMFAMILY'

PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBOzahmCOMMKZCdZCVK9eZBv6Ybgu0PhpatU7ZAO7yT5dXJwZAKXkv4iOC5ZBL58TkPc7ey2umnJLfQUdZCaWRaoBLGgoZA5d0xpumRRR3Cu3RWPT9PeIGWysbFCj69gYCBHOcylXTMCHIjpAPZBY5NrpeBkgxjTj0ZB9F5JFhux11H4zmqdT2XZBEkkd5mwv9KiHVqMvUfZCH7au3itBPkndGSHaKPtAZD'
user_preferences = {}


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


def handle_file_upload(request, wa_id):
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    if file:
        filename = os.path.join('uploads', f'{wa_id}_{file.filename}')
        file.save(filename)
        return filename


def handle_role_selection(message_body, wa_id):
    if message_body in ['1', '2']:
        roles = ['Farmer', 'Dealer']
        selected_role = roles[int(message_body) - 1]
        user_preferences[wa_id]['role_selected'] = selected_role

        if selected_role == 'Farmer':
            send_msg(
                'You have selected the role: Farmer. Please provide your Aadhar Card and Satbara pdf.', wa_id)
        elif selected_role == 'Dealer':
            send_msg(
                'You have selected the role: Dealer. Please provide your License number and Aadhar details.', wa_id)
    else:
        send_msg('Sorry, I did not understand your role selection. Please select a valid option: 1. Farmer, 2. Dealer', wa_id)


def handle_document_selection(message_body, wa_id):
    if 'role_selected' in user_preferences.get(wa_id, {}):
        selected_role = user_preferences[wa_id]['role_selected']
        if selected_role == 'Farmer' and message_body in ['1', '2']:
            document_options = ['Aadhar', 'Satbara']
            selected_document = document_options[int(message_body) - 1]
            user_preferences[wa_id]['document_selected'] = selected_document
            send_msg(
                f'You have selected the document: {selected_document}. Now, please upload the {selected_document} file.', wa_id)
        elif selected_role == 'Dealer' and message_body in ['1', '2']:
            document_options = ['License', 'Aadhar']
            selected_document = document_options[int(message_body) - 1]
            user_preferences[wa_id]['document_selected'] = selected_document
            send_msg(
                f'You have selected the document: {selected_document}. Now, please upload the {selected_document} file.', wa_id)
        else:
            send_msg('Sorry, I did not understand your document selection. Please select a valid option: 1. Aadhar, 2. Satbara (for Farmer) or 1. License, 2. Aadhar (for Dealer)', wa_id)
    else:
        send_msg('Sorry, I cannot process the document selection without a selected role. Please select a role first.', wa_id)


def handdle_select_menu():

    pass


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
                    contacts = message_value.get('contacts', [])
                    if message_value:
                        messages = message_value.get('messages', [])
                        if contacts:
                            wa_id = contacts[0].get('wa_id')
                            phn = "+" + validate_user(wa_id)
                            if not wa_id:
                                return jsonify({'status': 'error', 'message': 'wa_id not found'})

                        if messages:
                            sender_id = messages[0].get('from')
                            message_body = messages[0]['text']['body'].lower() if messages and messages[0].get(
                                'text') and 'body' in messages[0]['text'] else None
                            print("Message Body:", message_body)
                            print("Type of message_body:", type(message_body))
                            if 'language_selected' not in user_preferences.get(wa_id, {}):
                                handle_language_selection(message_body, wa_id)
                            elif 'role_selected' not in user_preferences.get(wa_id, {}):
                                handle_role_selection(message_body, wa_id)
                            else:
                                send_msg(
                                    'Sorry, I did not understand your message.', wa_id)

                            if 'document_selected' not in user_preferences.get(wa_id, {}):
                                handle_document_selection(message_body, wa_id)
                            else:
                                send_msg(
                                    'Sorry, I did not understand your message.', wa_id)
                            if message_body == '1':
                                send_msg(
                                    'Please upload the file.', wa_id)
                                filename = handle_file_upload(request, wa_id)
                                print("Filename:", filename)
                                send_msg(
                                    f'File uploaded successfully. Filename: {filename}', wa_id)
                            else:
                                send_msg(
                                    'Sorry, I did not understand your message.', wa_id)

        except Exception as e:
            print(f"Error: {e}")
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

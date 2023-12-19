from flask import Flask, request, jsonify
import requests
import os
import logging


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

VERIFY_TOKEN = 'KMFAMILY'

PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBO5eNpXZCtPAJTYvNl2IxxDshgLkHn6sVUvyoDhIdDMr8M6x7OwvvaKKsfTVxmDUOVZC4GiS8PRx0woUyaZAsBZATXJGo0UiMuWPQ1pfZAgITM25xG1ZBp6hX6SWiezvufKMIfK2UIU0e838o8FHWznZC8CuyAxtTorg4OxQh3FKDRwcMaaGwvj9ZBCqCMLbeqUhOttZB2d9IGrUGdLkOi8KUVoFAZD'
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
        'document_verification': ' Verification sucessfull',
        'document_validation_failed': 'Sorry, we could not validate your documents. Please try again.',
        'select_hangam': 'Select Hangam: 1. Kharip, 2. Rabii',
        'hangam_selected_kharip': 'You have selected Kharip hangam.',
        'hangam_selected_rabii': 'You have selected Rabii hangam.',
        'Main_menu_farmer': '1. Crop Prediction  \n 2. Suggestion of Government Schemes \n 3. Nearest APMC \n 4. Industry Recommendation',
        'Main_menu_dealer': '1. Probable Profit \n 2. Industry Recommendation',



        'enter_values': 'Please enter the following values 1. Nitrogen 2. Phosphorous 3. Potassium 4. Temperature 5. Humidity 6. PH 7. Rainfall',

        'enter_nitrogen': 'Enter the nitrogen value',
        'enter_phosphorous': 'Enter the phosphorous value',
        'enter_potassium': 'Enter the potassium value',
        'enter_temperature': 'Enter the temperature value',
        'enter_humidity': 'Enter the humidity value',
        'enter_ph': 'Enter the ph value',
        'enter_rainfall': 'Enter the rainfall value',




    },
    'hi': {
        'welcome': 'स्वागत है! कृपया भाषा का चयन करें: 1. इंग्लिश, 2. हिंदी, 3. मराठी।',
        'invalid_option': 'क्षमा करें, मैंने आपके संदेश को समझा नहीं। कृपया एक वैध विकल्प चुनें।',
        'role_selection': 'कृपया एक भूमिका का चयन करें: 1. किसान, 2. डीलर',
        'upload_documents_farmer': 'कृपया खेती के लिए अपना आधार कार्ड और सतबारा पीडीएफ अपलोड करें।',
        'upload_documents_dealer': 'कृपया डीलरशिप के लिए अपना लाइसेंस नंबर और आधार विवरण अपलोड करें।',
        'documents_uploaded_farmer': 'अपने दस्तावेज़ अपलोड करने के लिए धन्यवाद। हम जल्द ही आपसे संपर्क करेंगे।',
        'documents_uploaded_dealer': 'अपने दस्तावेज़ अपलोड करने के लिए धन्यवाद। हम जल्द ही आपसे संपर्क करेंगे।',
        'document_verification': ' apka verification hogaya hai ',
        'documents_uploaded': 'अपने दस्तावेज़ अपलोड करने के लिए धन्यवाद। हम जल्द ही आपसे संपर्क करेंगे।',
        'select_hangam': 'आप हैंगम का चयन करें: 1. खरीप, 2. रबी',
        'hangam_selected_kharip': 'आपने खरीप हैंगम का चयन किया है।',
        'hangam_selected_rabii': 'आपने रबी हैंगम का चयन किया है।',
        'Main_menu_farmer': '1. फसल की भविष्यवाणी \n 2. सरकारी योजनाओं का सुझाव \n 3. निकटतम एपीएमसी \n 4. उद्योग की सिफारिश',
        'Main_menu_dealer': '1. संभावित लाभ \n 2. उद्योग की सिफारिश',
        'enter_values': 'कृपया निम्नलिखित मानों को दर्ज करें 1. नाइट्रोजन 2. फॉस्फोरस 3. पोटैशियम 4. तापमान 5. आर्द्रता 6. पीएच 7. वर्षा',

        'enter_nitrogen': "नाइट्रोजन का मान दर्ज करें",
        'enter_phosphorous': "फॉस्फोरस का मान दर्ज करें",
        'enter_potassium': "पोटेशियम का मान दर्ज करें",
        'enter_temperature': "तापमान का मान दर्ज करें",
        'enter_humidity': "आर्द्रता का मान दर्ज करें",
        'enter_ph': "पीएच का मान दर्ज करें",
        'enter_rainfall': "वर्षा का मान दर्ज करें"

    },
    'mr': {
        'welcome': 'स्वागत आहे! कृपया भाषा निवडा: 1. इंग्लिश, 2. हिंदी, 3. मराठी.',
        'invalid_option': 'माफ करा, मला तुमचा संदेश समजला नाही. कृपया एक वैध पर्याय निवडा.',
        'role_selection': 'कृपया एक भूमिका निवडा: 1. शेतकरी, 2. डीलर',
        'upload_documents_farmer': 'कृपया कृषिक्षेत्रात आपला आधार कार्ड आणि सातबारा पीडीएफ अपलोड करा।',
        'upload_documents_dealer': 'कृपया व्यापारीक्षेत्रात आपला लायसेंस नंबर आणि आधार विवरण अपलोड करा।',
        'documents_uploaded_farmer': 'आपले दस्तावेज अपलोड करण्याबद्दल धन्यवाद. आम्ही लवकरच आपल्याशी संपर्क साधू.',
        'documents_uploaded_dealer': 'आपले दस्तावेज अपलोड करण्याबद्दल धन्यवाद. आम्ही लवकरच आपल्याशी संपर्क साधू.',
        'document_verification': ' aple verifcication zale ahe ',
        'documents_uploaded': 'आपले दस्तावेज अपलोड करण्याबद्दल धन्यवाद. आम्ही लवकरच आपल्याशी संपर्क साधू.',
        'select_hangam': 'हंगाम निवडा: 1. खरीप, 2. रबी',
        'hangam_selected_kharip': 'तुमची निवड: खरीप हंगाम.',
        'hangam_selected_rabii': 'तुमची निवड: रबी हंगाम.',
        'Main_menu_farmer': '1. पीक अंदाज \n 2. सरकारी योजनांचा सुचवणी \n 3. निकटतम एपीएमसी \n 4. उद्योग सिफारिश',
        'Main_menu_dealer': '1. संभाव्य फायदा \n 2. उद्योग सिफारिश',
        'enter_values': 'कृपया खालील मूल्ये प्रविष्ट करा 1. नाइट्रोजन 2. फॉस्फरस 3. पोटॅशियम 4. तापमान 5. आर्द्रता 6. पीएच 7. पावसाचे मूल्य',
        'enter_nitrogen': "नाइट्रोजनचे मूल्य प्रविष्ट करा",
        'enter_phosphorous': "फॉस्फरसचे मूल्य प्रविष्ट करा",
        'enter_potassium': "पोटॅशियमचे मूल्य प्रविष्ट करा",
        'enter_temperature': "तापमानचे मूल्य प्रविष्ट करा",
        'enter_humidity': "आर्द्रतेचे मूल्य प्रविष्ट करा",
        'enter_ph': "पीएचचे मूल्य प्रविष्ट करा",
        'enter_rainfall': "पावसाचे मूल्य प्रविष्ट करा"
    },
}


MESSAGE_WELCOME = 'welcome'
MESSAGE_INVALID_OPTION = 'invalid_option'
MESSAGE_ROLE_SELECTION = 'role_selection'
MESSAGE_UPLOAD_DOCUMENTS = 'upload_documents'
MESSAGE_HANGAM_SELECTION = 'select_hangam'
MESSAGE_DOCUMENT_VERIFICATION = 'document_verification'
MESSAGE_MAIN_MENU_FARMER = 'Main_menu_farmer'
MESSAGE_MAIN_MENU_DEALER = 'Main_menu_dealer'

MESSAGE_ENTER_VALUES = 'enter_values'
MESSAGE_ENTER_NITROGEN = 'enter_nitrogen'
MESSAGE_ENTER_PHOSPHOROUS = 'enter_phosphorous'
MESSAGE_ENTER_POTASSIUM = 'enter_potassium'
MESSAGE_ENTER_TEMPERATURE = 'enter_temperature'
MESSAGE_ENTER_HUMIDITY = 'enter_humidity'
MESSAGE_ENTER_PH = 'enter_ph'
MESSAGE_ENTER_RAINFALL = 'enter_rainfall'


@app.route('/')
def index():
    return "Hello"


def get_wa_id(message_value):
    contacts = message_value.get('contacts', [])
    if contacts:
        return contacts[0].get('wa_id')
    return None


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


def genrate_media_url(media_id, wa_id):
    headers = {
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    response = requests.get(
        f'https://graph.facebook.com/v13.0/{media_id}?phone_number_id=135179146337629', headers=headers)
    media_url = response.json()['url']
    get_image(media_url)
    userlang = user_preferences.get(wa_id, {}).get('language_selected')
    send_msg(MESSAGE_HANGAM_SELECTION, wa_id, userlang)
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
        'http://192.168.121.120:60000', files=files)
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
    response = requests.post(
        'http://172.30.69.161:60001/extract', json=data)
    if response.status_code == 200:
        logging.info(response.json)
        return response.json()
    else:
        print(
            f"Failed to extract data. Status code: {response.status_code}, Error: {response.text}")
        return None


def handle_role_selection(message_body, wa_id):
    if message_body in ['1', '2']:
        roles = ['Farmer', 'Dealer']
        selected_role = roles[int(message_body) - 1]
        user_preferences.setdefault(wa_id, {})
        user_preferences[wa_id]['role_selected'] = selected_role
        user_preferences[wa_id]['documents_uploaded'] = False
        selected_language = user_preferences.get(
            wa_id, {}).get('language_selected', 'en')

        if selected_role in ['Farmer', 'Dealer']:
            msg_key = MESSAGE_UPLOAD_DOCUMENTS + f'_{selected_role.lower()}'
            send_msg(msg_key, wa_id, selected_language)
        else:
            handle_hangam_selection(message_body, wa_id)


def handle_hangam_selection(message_body, wa_id):
    if message_body in ['1', '2']:
        hangam_options = ['kharip', 'rabii']
        selected_hangam = hangam_options[int(message_body) - 1]
        user_preferences.setdefault(wa_id, {})
        user_preferences[wa_id]['hangam_selected'] = selected_hangam
        selected_language = user_preferences.get(
            wa_id, {}).get('language_selected', 'en')
        msg_key = f'hangam_selected_{selected_hangam.lower()}'
        send_msg(msg_key, wa_id, selected_language)
        selected_role = user_preferences.get(wa_id, {}).get('role_selected')
        logging.info(selected_role)

        if selected_role == 'Farmer':
            msg_key = MESSAGE_MAIN_MENU_FARMER
            send_msg(msg_key, wa_id, selected_language)
            main_menu(message_body, wa_id)

        elif selected_role == 'Dealer':
            msg_key = MESSAGE_MAIN_MENU_DEALER
            send_msg(msg_key, wa_id, selected_language)


def crop_prdection(wa_id, message_body):
    logging.info("crop prediction ")
    print(message_body)


def government_schemes():

    logging.info("government schemes")

    return None


def nearest_apmc():
    logging.info("nearest apmc")

    return None


def industry_recommendation():

    logging.info("industry recommendation")
    return None


def main_menu(message_body, wa_id):

    if message_body in ['1', '2', '3', '4']:
        main_menu_options = ['Crop Prediction', 'Suggestion of Government Schemes',
                             'Nearest APMC', 'Industry Recommendation']
        user_lang = user_preferences.get(wa_id, {}).get('language_selected')

        print(message_body)
        selected_main_menu = main_menu_options[int(message_body) - 1]
        logging.info(selected_main_menu)

        if message_body == '1':
            crop_prdection(wa_id, message_body)

        elif message_body == '2':
            government_schemes()


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
                    if 'messages' in message_value:
                        for message in message_value['messages']:
                            if 'image' in message:
                                media_id = message['image']['id']
                                contacts = message_value.get('contacts', [])
                                if contacts:
                                    wa_id = contacts[0].get('wa_id')
                                    userlang = user_preferences.get(
                                        wa_id, {}).get('language_selected')
                                    if media_id is not None:
                                        print(user_preferences)
                                        genrate_media_url(media_id, wa_id)
                                        message_key = MESSAGE_DOCUMENT_VERIFICATION
                                        send_msg(message_key, wa_id, userlang)
                                    if not wa_id:
                                        return jsonify({'status': 'error', 'message': 'wa_id not found'})
                                    message_body = message['text']['body'].lower(
                                    )
                            elif 'text' in message:
                                contacts = message_value.get('contacts', [])
                                if contacts:
                                    wa_id = contacts[0].get('wa_id')
                                    phn = "+" + validate_user(wa_id)
                                    if not wa_id:
                                        return jsonify({'status': 'error', 'message': 'wa_id not found'})
                                    message_body = message['text']['body'].lower(
                                    )
                                    print(message_body)
                                    if 'language_selected' not in user_preferences.get(wa_id, {}):
                                        handle_language_selection(
                                            message_body, wa_id)
                                    elif 'role_selected' not in user_preferences.get(wa_id, {}):
                                        handle_role_selection(
                                            message_body, wa_id)
                                    elif 'hangam_selected' not in user_preferences.get(wa_id, {}):
                                        handle_hangam_selection(
                                            message_body, wa_id)

                            else:
                                print("Unsupported message type")
        except Exception as e:
            print(f"Error: {e}")
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

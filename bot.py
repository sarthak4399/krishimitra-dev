from flask import Flask, request, jsonify
import requests
import os
import logging
import time

app = Flask(__name__)

VERIFY_TOKEN = "KMFAMILY"
user_preferences = {}
PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBOzVqMLmZBf80lClUCFc09EMEaEXPBt7ZA32Hjh8rppGn7ZAArDnLnL1f21Qo8QpedGddnJEbSE27XQOivFg8eMkguaz7uUdR553ytXvhCNDD6hgm5LcXQ6xwQ1kfpGuw7cEPOHkSKqZBjTGormoq06DZCxxr1CZBkGBgjZB7gr6dElZBVK0H97p58k20D1F5EXZCmp3IFQFZBX4AiKzD3FYwIHVbAZD'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MESSAGE_DOCUMENT_VERIFICATION = "your_message_document_verification"
messages = {
    'en': {
        'welcome': 'Welcome! Please select a language: 1. English, 2. Hindi, 3. Marathi.',
        'invalid_option': 'Sorry, I did not understand your message. Please select a valid option.',
        'role_selection': 'Please select a role: 1. Farmer, 2. Dealer ,3. FPO',
        'upload_documents_farmer': 'Please upload your Aadhar Card and Satbara pdf for farming.',
        'upload_documents_dealer': 'Please upload your License number and Aadhar details for dealership.',
        'upload_documents_fpo': 'Please upload your Documents for FPO.',
        'documents_uploaded_farmer': 'Thank you for uploading your documents. We will get back to you shortly.',
        'documents_uploaded_dealer': 'Thank you for uploading your documents. We will get back to you shortly.',
        'document_uplodeded_FPO': 'Thank you for uploading your documents. We will get back to you shortly',
        'documents_uploaded': 'Thank you for uploading your documents. We will get back to you shortly.',
        'document_verification': ' Verification sucessfull',
        'document_validation_failed': 'Sorry, we could not validate your documents. Please try again.',
        'select_hangam': 'Select Hangam: 1. Kharip, 2. Rabii',
        'hangam_selected_kharip': 'You have selected Kharip hangam\n ',
        'hangam_selected_rabii': 'You have selected Rabii hangam\n ',
        'Main_menu_farmer': ' Farmers Main Menu \n 1.Connect FPO and Industry   \n 2.Crop Prediction  \n 3. Nearest APMC \n 4. Industry Recommendation \n 5.Suggestion of Government Schemes',
        'Main_menu_dealer': '1.Probable Profit \n 2.Industry Recommendation',
        'Main_menu_FPO': '1.Sell Crop \n 2. Connect to FarmerBye Machinery \n 3.Industry Recommendation \n 4. Connect to Industry \n 5. ',
        'Enter_FPO': 'Enter the FPO name',
        'Enter_your_comodiity': 'Select the comodity crop to sell ',
        'Main_menu_FPO': '1.Sell Crop \n 2. Connect to FarmerBye Machinery \n 3.Industry Recommendation \n 4. Connect to Industry \n 5. ',
        'enter_values': 'Please enter the following values 1. Nitrogen 2. Phosphorous 3. Potassium 4. Temperature 5. Humidity 6. PH 7. Rainfall',
        'enter_nitrogen': 'Suggested FPO  https://chat.whatsapp.com/BVRrgtZJBXdDb1SGmq8Jgf',
        'enter_phosphorous': 'Enter the phosphorous value',
        'enter_potassium': 'Enter the potassium value',
        'enter_temperature': 'Enter the temperature value',
        'enter_humidity': 'Enter the humidity value',
        'enter_ph': 'Enter the ph value',
        'enter_rainfall': 'Enter the rainfall value',
        'comodity_options': '1. Rice \n 2. Soyabean \n 3. Cotton \n 4. Wheat',
        'suggested_FPO': 'Suggested FPO nearby to your location Click on the links below to connect with them  \n FPO 1.https://chat.whatsapp.com/BVRrgtZJBXdDb1SGmq8Jgf \n FPO 2. https://chat.whatsapp.com/ITSH16ekG4z1RMn5iqfRUE \n FPO 3.https://chat.whatsapp.com/JKJWy2bVftvAqpfLSQTGvO',
        'main_menu_callback': 'Back to Main menu 1.Yes \n 2.No',
        'crop_prediction': 'Crop Prediction \n 1. Rice \n 2. Soyabean \n 3. Cotton \n 4. Wheat',


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
MESSAGE_MAIN_MENU_FPO = 'Main_menu_FPO'
MESSAGE_SELECT_FPO = 'Enter_FPO'
MESSA_FPO_MENU = 'Main_menu_FPO'
MESSAGE_ENTER_VALUES = 'enter_values'
MESSAGE_ENTER_NITROGEN = 'enter_nitrogen'
MESSAGE_ENTER_PHOSPHOROUS = 'enter_phosphorous'
MESSAGE_ENTER_POTASSIUM = 'enter_potassium'
MESSAGE_ENTER_TEMPERATURE = 'enter_temperature'
MESSAGE_ENTER_HUMIDITY = 'enter_humidity'
MESSAGE_ENTER_PH = 'enter_ph'
MESSAGE_ENTER_RAINFALL = 'enter_rainfall'
MESSAGE_COONNECT_TO_FPO_NO = 'connect_FPO_no'
MESSAGE_COMMODITY = 'Enter_your_comodiity'
MESSAGE_COMMODITY_OPTIONS = 'comodity_options'

MESSAGE_SUGGESTED_FPO = 'suggested_FPO'
MESSAGE_MAIN_MENU_CALLBACK = 'main_menu_callback'
MESSAGE_CROP_PREDICTION = 'crop_prediction'


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
                       '+919492235028', '+918446901953', '+918291798609', '+918177834839']
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
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')


def genrate_media_url(media_id, wa_id):
    headers = {
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    response = requests.get(
        f'https://graph.facebook.com/v13.0/{media_id}?phone_number_id=135179146337629', headers=headers)
    media_url = response.json()['url']

    get_image(media_url)
    logging.info(media_url)
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
        file_path = f"image.{file_extension}"
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded and saved to: {file_path}")
        upload_image(file_path)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def upload_image(file_path):
    files = {'photo': open(file_path, 'rb')}
    response = requests.post(
        'http://172.30.69.161:60000/upload', files=files)

    if response.status_code == 200:
        public_url = response.json().get('public_url')
        print(f"Image uploaded successfully. Public URL: {public_url}")
        extract_data(public_url)


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
    if message_body in ['1', '2', '3']:
        roles = ['Farmer', 'Dealer', 'Fpo']
        selected_role = roles[int(message_body) - 1]
        user_preferences.setdefault(wa_id, {})
        user_preferences[wa_id]['role_selected'] = selected_role
        user_preferences[wa_id]['documents_uploaded'] = False
        selected_language = user_preferences.get(
            wa_id, {}).get('language_selected', 'en')
        if selected_role in ['Farmer', 'Dealer', 'FPO']:
            msg_key = MESSAGE_UPLOAD_DOCUMENTS + f'_{selected_role.lower()}'
            print(msg_key)
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
            send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, selected_language)
        elif selected_role == 'Dealer':
            send_msg(MESSAGE_MAIN_MENU_DEALER, wa_id, selected_language)
        elif selected_role == 'Fpo':
            send_msg(MESSA_FPO_MENU, wa_id, selected_language)
        else:
            handle_hangam_selection(message_body, wa_id)
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')


def crop_prdection(message_body, wa_id):
    logging.info("crop prediction ")
    userlang = user_preferences.get(wa_id, {}).get('language_selected')
    send_msg(MESSAGE_CROP_PREDICTION, wa_id, userlang)


def government_schemes():

    logging.info("government schemes")

    return None


def nearest_apmc():
    logging.info("nearest apmc")

    return None


def industry_recommendation():

    logging.info("industry recommendation")
    return None


def create_community():
    logging.info("create community")
    # url = f"{BASE_URL}groups?token={PAGE_ACCESS_TOKEN}"
    # data = {"subject": subject, "participants": participants}
    # headers = {"accept": "application/json",
    #            "content-type": "application/json"}

    # response = requests.post(url, json=data, headers=headers)

    # if response.status_code == 201:
    #     return response.json()  # Return group details on success
    # else:
    #     raise Exception(f"Failed to create group: {response.text}")
    return None


def connect_to_industry(message_body, wa_id):
    logging.info("connect to industry")

    send_msg(MESSAGE_SELECT_FPO, wa_id, 'en')

    return None


def connect_FPO(message_body, wa_id):
    print(message_body)
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>connect FPO")
    userlang = user_preferences.get(wa_id, {}).get('language_selected')


def main_menu(message_body, wa_id):
    if message_body in ['1', '2', '3', '4', '5']:
        selected_language = user_preferences.get(
            wa_id, {}).get('language_selected', 'en')
        options = ['Connect FPO and Industry', 'Crop Prediction',
                   'Nearest APMC', 'Industry Recommendation', 'Suggestion of Government Schemes']
        selected_option = options[int(message_body) - 1]
        user_preferences[wa_id]['selected_option'] = selected_option
        selected_role = user_preferences.get(wa_id, {}).get('role_selected')
        logging.info(selected_role)
        if selected_role == 'Farmer':
            if selected_option == 'Connect FPO and Industry':

                send_msg(MESSAGE_SUGGESTED_FPO, wa_id, selected_language)
                send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, selected_language)

            elif selected_option == 'Crop Prediction':
                crop_prdection(message_body, wa_id)

            elif selected_option == 'Suggestion of Government Schemes':
                government_schemes()

            elif selected_option == 'Nearest APMC':
                nearest_apmc()

            elif selected_option == 'Industry Recommendation':
                industry_recommendation()

            else:
                main_menu(message_body, wa_id)

        elif selected_role == 'FPO':
            if selected_option == '1':
                create_community()
            elif selected_option == '2':
                connect_to_industry()


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return handle_verification(request)
    elif request.method == 'POST':
        return handle_messages(request)


def handle_verification(request):
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return 'Invalid verification token'


def handle_messages(request):
    try:
        res = request.get_json()
        if 'entry' in res and res['entry']:
            for entry in res['entry']:
                for change in entry.get('changes', []):
                    if 'value' in change and 'messages' in change['value']:
                        for message_value in change['value']['messages']:
                            handle_message(message_value)

    except Exception as e:
        print(f"Error: {e}")
    return jsonify({'status': 'success'})


def get_message_values(changes):
    return [change['value'] for change in changes if 'messages' in change['value']]


def handle_message(message_value):
    print(message_value)
    if 'image' in message_value:
        handle_image_message(message_value)
    elif 'text' in message_value:
        handle_text_message(message_value)
    else:
        print("Unsupported message type")


def handle_image_message(message_value):
    media_id = message_value.get('image', {}).get('id')
    contacts = message_value.get('contacts', [])
    if contacts:
        wa_id = contacts[0].get('wa_id')
        userlang = user_preferences.get(wa_id, {}).get('language_selected')
        if media_id is not None:
            genrate_media_url(media_id, wa_id)
            message_key = MESSAGE_DOCUMENT_VERIFICATION
            send_msg(message_key, wa_id, userlang)
        else:
            print("Media ID not found")


def handle_text_message(message_value):
    print(message_value)

    wa_id = message_value.get('from', '')  # 'from' is the phone number
    phn = "+" + validate_user(wa_id)
    if not wa_id:
        return jsonify({'status': 'error', 'message': 'wa_id not found'})

    message_body = message_value.get('text', {}).get('body', '').lower()
    print(user_preferences)
    handle_user_preferences(wa_id, message_body)


def handle_user_preferences(wa_id, message_body):
    if 'language_selected' not in user_preferences.get(wa_id, {}):
        handle_language_selection(message_body, wa_id)
    elif 'role_selected' not in user_preferences.get(wa_id, {}):
        handle_role_selection(message_body, wa_id)
    elif 'hangam_selected' not in user_preferences.get(wa_id, {}):
        handle_hangam_selection(message_body, wa_id)
    elif 'selected_option' not in user_preferences.get(wa_id, {}):
        main_menu(message_body, wa_id)
    elif 'commodity_selected' not in user_preferences.get(wa_id, {}):
        connect_FPO(wa_id, message_body)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

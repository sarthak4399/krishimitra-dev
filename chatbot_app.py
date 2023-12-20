from flask import Flask, request, jsonify
import requests
import os
import logging
import time


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

VERIFY_TOKEN = 'KMFAMILY'

PAGE_ACCESS_TOKEN = 'EAAJztZAX6JRwBOzVqMLmZBf80lClUCFc09EMEaEXPBt7ZA32Hjh8rppGn7ZAArDnLnL1f21Qo8QpedGddnJEbSE27XQOivFg8eMkguaz7uUdR553ytXvhCNDD6hgm5LcXQ6xwQ1kfpGuw7cEPOHkSKqZBjTGormoq06DZCxxr1CZBkGBgjZB7gr6dElZBVK0H97p58k20D1F5EXZCmp3IFQFZBX4AiKzD3FYwIHVbAZD'
user_preferences = {}

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
messages = {
    'en': {
        'welcome': 'Welcome! Please select a language: 1. English, 2. Hindi, 3. Marathi.',
        'invalid_option': 'Sorry, I did not understand your message. Please select a valid option.',
        'role_selection': 'Please select a role: \n1. Farmer\n2. Dealer \n 3. FPO',
        'upload_documents_farmer': 'Please upload your Aadhar Card for farming.',
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
        'Main_menu_FPO': '1. Sell Crop \n 2. Connect to Farmer Bye Machinery \n 3 .Industry Recommendation \n 4 .Connect to Industry \n 5.Accept instreseted Farmer',
        'Enter_FPO': 'Enter the FPO name',
        'Enter_your_comodiity': 'Select the comodity crop to sell ',
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
        'government_schemes': 'Suggestion of Government Schemes \n 1. PM Kisan Samman Nidhi Yojana \n 2. Pradhan Mantri Fasal Bima Yojana \n 3. Pradhan Mantri Krishi Sinchai Yojana \n 4. Paramparagat Krishi Vikas Yojana \n 5. Kisan Credit Card Scheme \n 6. Pradhan Mantri Kisan Maandhan Yojana \n 7. Pradhan Mantri Kisan Sampada Yojana \n 8. Rashtriya Krishi Vikas Yojana \n 9. National Food Security Mission \n 10. Pradhan Mantri Annadata Aay Sanrakshan Abhiyan',
        'nearest_apmc': 'Nearest APMC \n1 .MSWC, Ratnali Road, Dharmabad, A/P Dharmabad, Tal.Dharmabad, Dist.Nanded 431809 Off. Tel No. 02465-24368, 9975890271 MSWC,\n2. Mahur Road, A/P Kinwat, Tal.Kinwat, Dist.Nanded 431804 Off. Tel No. 9130777957 ',
        'industry_recommendation': 'Industry Recommendation \n 1. Rice \n 2. Soyabean \n 3. Cotton \n 4. Wheat',

    },
    'hi': {
        'welcome': 'स्वागत है! कृपया भाषा का चयन करें: 1. इंग्लिश, 2. हिंदी, 3. मराठी।',
        'invalid_option': 'क्षमा करें, मैंने आपके संदेश को समझा नहीं। कृपया एक वैध विकल्प चुनें।',
        'role_selection': 'कृपया एक भूमिका का चयन करें: 1. किसान, 2. डीलर 3. एफपीओ  ',
        'upload_documents_farmer': 'कृपया खेती के लिए अपना आधार कार्ड अपलोड करें।',
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
        'enter_rainfall': "वर्षा का मान दर्ज करें",
        'comodity_options': '1. चावल \n 2. सोयाबीन \n 3. कपास \n 4. गेहूं',
        'government_scheme': 'सरकारी योजनाओं के सुझाव \n 1. पीएम किसान सम्मान निधि योजना \n 2. प्रधानमंत्री फसल बीमा योजना \n 3. प्रधानमंत्री कृषि सिंचाई योजना \n 4. परंपरागत कृषि विकास योजना \n 5. किसान क्रेडिट कार्ड योजना \n 6. प्रधानमंत्री किसान मानधन योजना \n 7. प्रधानमंत्री किसान संपदा योजना \n 8. राष्ट्रीय कृषि विकास योजना \n 9. राष्ट्रीय खाद्य सुरक्षा मिशन \n 10. प्रधानमंत्री अन्नदाता आय संरक्षण अभियान',
        'nearest_apmc': 'निकटतम APMC \n1. एमएसडब्ल्यूसी, रत्नाली रोड, धर्माबाद, आ / पी धर्माबाद, ता. धर्माबाद, जि. नांदेड 431809 ऑफ. टेल नंबर 02465-24368, 9975890271 एमएसडब्ल्यूसी,\n2. महूर रोड, आ / पी किनवट, ता. किनवट, जि. नांदेड 431804 ऑफ. टेल नंबर 9130777957',
        'industry_recommendation': 'उद्योग की सिफारिश \n 1. चावल \n 2. सोयाबीन \n 3. कपास \n 4. गेहूं',

    },
    'mr': {
        'welcome': 'स्वागत आहे! कृपया भाषा निवडा: 1. इंग्लिश, 2. हिंदी, 3. मराठी.',
        'invalid_option': 'माफ करा, मला तुमचा संदेश समजला नाही. कृपया एक वैध पर्याय निवडा.',
        'role_selection': 'कृपया एक भूमिका निवडा: 1. शेतकरी, 2. डीलर 3. एफपीओ',
        'upload_documents_farmer': 'कृपया कृषिक्षेत्रात आपला आधार कार्ड अपलोड करा।',
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
        'enter_rainfall': "पावसाचे मूल्य प्रविष्ट करा",
        'government_scheme': 'सरकारच्या योजनांची सुची \n 1. पीएम किसान सम्मान निधि योजना \n 2. प्रधानमंत्री फसल बीमा योजना \n 3. प्रधानमंत्री कृषि सिंचाई योजना \n 4. परंपरागत कृषि विकास योजना \n 5. किसान क्रेडिट कार्ड योजना \n 6. प्रधानमंत्री किसान मांडण योजना \n 7. प्रधानमंत्री किसान संपदा योजना \n 8. राष्ट्रीय कृषि विकास योजना \n 9. राष्ट्रीय खाद्य सुरक्षा मिशन \n 10. प्रधानमंत्री अन्नदाता आय संरक्षण अभियान',
        'nearest_apmc': 'निकटतम APMC \n1. एमएसडब्ल्यूसी, रत्नाळी रोड, धर्माबाद, आ / पी धर्माबाद, ता. धर्माबाद, जि. नांदेड 431809 ऑफ. टेल नंबर 02465-24368, 9975890271 एमएसडब्ल्यूसी,\n2. महूर रोड, आ / पी किनवट, ता. किनवट, जि. नांदेड 431804 ऑफ. टेल नंबर 9130777957',
        'industry_recommendation': 'उद्योग सिफारिश \n 1. चावल \n 2. सोयाबीन \n 3. कपास \n 4. गेहूं',
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
MESSAGE_FPO_DOCUMENTS = 'upload_documents_fpo'

MESSAGE_FPO_DOCUMENTS_FPO = 'upload_documents_fpo'
MESSAGE_UPLOAD_DOCUMENTS_FARMERS = 'upload_documents_farmer'
MESSAGE_UPLOAD_DOCUMENTS_DEALERS = 'upload_documents_dealer'
MESSAGE_GOVERNMENT_SCHEMES = 'government_schemes'
NEAREST_APMC = 'nearest_apmc'
MESSAGE_INDUSTRY_RECOMMENDATION = 'industry_recommendation'
MESSA_FPO_MENU = 'Main_menu_FPO'


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
        send_msg(MESSAGE_WELCOME, wa_id, 'en')


def genrate_media_url(media_id, wa_id):

    print(">>>>>>>>>>>>>>>>>>>>>>>>iside the genrate media url ")
    if media_id != None:
        headers = {
            'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
        }
        response = requests.get(
            f'https://graph.facebook.com/v13.0/{media_id}?phone_number_id=135179146337629', headers=headers)
        media_url = response.json()['url']
        get_image(media_url)
        userlang = user_preferences.get(wa_id, {}).get('language_selected')
        message_key = MESSAGE_DOCUMENT_VERIFICATION
        print(f">>>>>>>>ABOve msg key ")
        send_msg(message_key, wa_id, userlang)
        print(f">>>>>>>>below msg key ")
        user_preferences[wa_id]['documents_uploaded'] = True

        send_msg(MESSAGE_HANGAM_SELECTION, wa_id, userlang)
        return media_url
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')
        send_msg(MESSAGE_UPLOAD_DOCUMENTS, wa_id, 'en')


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
        'http://172.30.69.161:60000/upload', files=files)
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
    if message_body in ['1', '2', '3']:
        roles = ['Farmer', 'Dealer', 'FPO']
        selected_role = roles[int(message_body) - 1]
        user_preferences.setdefault(wa_id, {})
        user_preferences[wa_id]['role_selected'] = selected_role
        user_preferences[wa_id]['documents_uploaded'] = False
        user_lang = user_preferences.get(wa_id, {}).get('language_selected')
        selected_language = user_preferences.get(
            wa_id, {}).get('language_selected', 'en')
        if selected_role == 'Farmer':
            send_msg(MESSAGE_UPLOAD_DOCUMENTS_FARMERS,
                     wa_id, selected_language)
        elif selected_role == 'Dealer':
            send_msg(MESSAGE_UPLOAD_DOCUMENTS_DEALERS,
                     wa_id, selected_language)
        elif selected_role == 'FPO':
            send_msg(MESSAGE_FPO_DOCUMENTS, wa_id, selected_language)

        else:
            handle_hangam_selection(message_body, wa_id)
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')
        send_msg(MESSAGE_ROLE_SELECTION, wa_id, 'en')


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
            # handle_hangam_selection(message_body, wa_id)
            send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')
        send_msg(MESSAGE_HANGAM_SELECTION, wa_id, 'en')


def crop_prdection(message_body, wa_id):
    logging.info("crop prediction ")
    userlang = user_preferences.get(wa_id, {}).get('language_selected')
    send_msg(MESSAGE_CROP_PREDICTION, wa_id, userlang)
    return None


def government_schemes(message_body, wa_id):
    logging.info("government schemes")
    send_msg(MESSAGE_GOVERNMENT_SCHEMES, wa_id, 'en')
    return None


def nearest_apmc(message_body, wa_id):
    logging.info("nearest apmc")
    send_msg(NEAREST_APMC, wa_id, 'en')
    return None


def industry_recommendation(message_body, wa_id):
    send_msg(MESSAGE_MAIN_MENU_DEALER, wa_id, 'en')
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
                send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, 'en')
                user_preferences[wa_id]['selected_option'] = {}
            elif selected_option == 'Crop Prediction':
                crop_prdection(message_body, wa_id)
                send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, 'en')
                user_preferences[wa_id]['selected_option'] = {}
            elif selected_option == 'Suggestion of Government Schemes':
                government_schemes(message_body, wa_id)
                send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, 'en')
                user_preferences[wa_id]['selected_option'] = {}

            elif selected_option == 'Nearest APMC':
                nearest_apmc(message_body, wa_id)
                send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, 'en')
                user_preferences[wa_id]['selected_option'] = {}

            elif selected_option == 'Industry Recommendation':
                industry_recommendation(message_body, wa_id)
                send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, 'en')
                user_preferences[wa_id]['selected_option'] = {}

            else:
                send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')

        elif selected_role == 'FPO':
            send_msg(MESSA_FPO_MENU, wa_id, 'en')

        elif selected_role == 'Dealer':
            send_msg(MESSAGE_MAIN_MENU_DEALER, wa_id, 'en')
    else:
        send_msg(MESSAGE_INVALID_OPTION, wa_id, 'en')
        # send_msg(MESSAGE_MAIN_MENU_FARMER, wa_id, 'en')


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
                                        print(f"media_id>>>>>>>"+media_id)

                                        genrate_media_url(media_id, wa_id)
                                    else:
                                        user_lang = user_preferences.get(
                                            wa_id, {}).get('language_selected')
                                        send_msg(
                                            MESSAGE_INVALID_OPTION, wa_id, 'en') and send_msg(
                                            MESSAGE_UPLOAD_DOCUMENTS, wa_id, 'en')
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
                                    # ###print(message_body)
                                    print(user_preferences)
                                if 'language_selected' not in user_preferences.get(wa_id, {}):
                                    handle_language_selection(
                                        message_body, wa_id)
                                elif 'role_selected' not in user_preferences.get(wa_id, {}):
                                    handle_role_selection(
                                        message_body, wa_id)
                                elif 'documents_uploaded' not in user_preferences.get(wa_id, {}):
                                    genrate_media_url(media_id, wa_id)
                                elif 'hangam_selected' not in user_preferences.get(wa_id, {}):
                                    handle_hangam_selection(
                                        message_body, wa_id)
                                elif 'selected_option' not in user_preferences.get(wa_id, {}):
                                    main_menu(message_body, wa_id)
                                elif 'commodity_selected' not in user_preferences.get(wa_id, {}):
                                    connect_FPO(wa_id, message_body)

                            else:
                                print("Unsupported message type")
        except Exception as e:
            print(f"Error: {e}")
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

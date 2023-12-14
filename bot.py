from flask import Flask, request, jsonify
import cv2
from pyzbar.pyzbar import decode
import pytesseract

app = Flask(__name__)


@app.route('/extract_aadhar_info', methods=['POST'])
def extract_aadhar_info():
    try:
        # Assuming the image is sent as a file in the request
        image = cv2.imdecode(np.fromstring(
            request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # Use pyzbar to decode QR code
        decoded_objects = decode(image)

        # Extract text from image using Tesseract OCR
        text = pytesseract.image_to_string(image)

        # You can further process the 'decoded_objects' and 'text' as needed

        # Return the extracted information as JSON
        return jsonify({'qr_code_data': [obj.data.decode('utf-8') for obj in decoded_objects], 'text_data': text})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

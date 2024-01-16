# AgroTech Solutions - Crop Prediction and Inventory Management System

## Overview

AgroTech Solutions is a comprehensive platform designed to mitigate excess crop sowing and raw material storage losses through timely crop predictions, buyer recommendations, and customized advice for farmers and dealers. The system employs advanced technologies, including AI/ML-driven recommendations, user validation through government-issued documents, GPS-based information, and timely alerts for effective inventory management.

## Key Features

### 1. **Timely Crop Predictions and Buyer Recommendations:**
   - Leverages machine learning algorithms for timely crop predictions for farmers.
   - Provides buyer recommendations for dealers based on market trends and historical data.

### 2. **Customized Advice:**
   - Customizes advice for users, reducing raw material waste and recommending crops in their preferred language.

### 3. **User Validation:**
   - Implements a secure user validation process using government-issued documents, ensuring the authenticity of users.

### 4. **AI/ML-Driven Recommendations:**
   - Tailors recommendations to specific user roles, utilizing advanced AI/ML models for personalized advice.

### 5. **GPS-Based Information:**
   - Offers GPS-based information, guiding users to the nearest Agriculture Produce Market Committee (APMC) for convenient transactions.

### 6. **Timely Alerts for Inventory Management:**
   - Sends timely alerts to manufacturers regarding product expiration, facilitating optimal inventory management.

### 7. **Broker Algorithm:**
   - Features an algorithm for brokers, recommending industries based on historical requirements to minimize storage losses.

## Technologies Used

- **Python (Programming Language):** The core programming language used for backend development.
- **Pyaadhar:** Utilized for user validation through government-issued documents.
- **Machine Learning:** Employed for crop predictions and AI/ML-driven recommendations.
- **Flask:** Used for building the web application and API.
- **OpenCV:** Applied for image processing tasks.
- **Amazon Web Services (AWS):** Hosts the platform, ensuring scalability and reliability.

## Skills Required

- **Python (Programming Language)**
- **Pyaadhar**
- **Machine Learning**
- **Flask**
- **Application Programming Interfaces (API)**
- **OpenCV**
- **Amazon Web Services (AWS)**

## Getting Started
Certainly! Below are the installation and running steps for the chatbot using Ngrok and Flask server based on the provided content:

## Installation and Running Steps for Chatbot

### Prerequisites

1. **Python 3.x:** Ensure that you have Python 3.x installed on your system.

2. **Ngrok:** Install Ngrok for exposing the local Flask server to the internet. You can download it from [https://ngrok.com/](https://ngrok.com/).

3. **Flask and Required Dependencies:** Install the necessary Python packages using the following command:

    ```bash
    pip install Flask
    ```

### Clone the Repository

```bash
git clone https://github.com/sarthak4399/krishimitra-dev.git
cd krishimitra-dev
```

### Update Configuration

Open the `chatbot_app.py` file and update any configuration parameters such as API keys or other settings if needed.

### Run the Flask Server

```bash
python chatbot_app.py
```

This will start the Flask server locally.

### Expose the Local Server with Ngrok

Open a new terminal window and navigate to the directory where Ngrok is located. Run the following command to expose the local Flask server:

```bash
./ngrok http 5000
```

Ngrok will provide a public URL (e.g., `https://your-ngrok-subdomain.ngrok.io`). Note this URL for the next step.

### Configure Twilio

1. Create a Twilio account if you don't have one: [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).

2. Set up a Twilio WhatsApp Sandbox: [https://www.twilio.com/docs/sms/whatsapp/sandbox](https://www.twilio.com/docs/sms/whatsapp/sandbox).

3. Update the WhatsApp Sandbox with the Ngrok URL obtained in the previous step.

### Run the Chatbot

Now, your chatbot is ready to receive and respond to messages on WhatsApp. Start a conversation with your Twilio WhatsApp number and interact with the chatbot.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the open-source communities and contributors in Python, Flask, Ngrok, Twilio and machine learning for their valuable tools and libraries.
- Thanks to the AWS team for providing reliable cloud services to host this innovative solution.

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and enhancements are highly appreciated!

from flask import Flask, jsonify, Blueprint
import requests
from requests.auth import HTTPBasicAuth
from config import Config 



mpesapay_routes = Blueprint('payment', __name__)

@mpesapay_routes.route('/pay', methods=['POST'])
def initiate_payment():
    # Fetch these from your database or some configuration
    CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
    CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
    shortcode = 'YOUR_SHORTCODE'
    lipa_na_mpesa_online_passkey = 'YOUR_PASSKEY'
    lipa_na_mpesa_online_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    # Generate access token
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth = HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    json_response = response.json()
    access_token = json_response['access_token']

    # Fetch the phone number and amount from your frontend
    phone = request.json['phone']
    amount = request.json['amount']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    request = {
        "BusinessShortCode": shortcode,
        "Password": "YOUR_GENERATED_PASSWORD",  # You will need a method to generate this.
        "Timestamp": "YOUR_GENERATED_TIMESTAMP", # Current timestamp
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://yourdomain.com/callback",
        "AccountReference": "YOUR_REFERENCE",
        "TransactionDesc": "Payment for services"
    }
    
    response = requests.post(lipa_na_mpesa_online_endpoint, json=request, headers=headers)
    
    return jsonify(response.json()), 200
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

CLIENT_ID = 'fa8e9c3ca1a845658a888ee89b0ff4f1'
CLIENT_SECRET = 'b0d568ffbe5e42bfb4ee7f33a9f96313'

@app.route('/authenticate', methods=['POST'])
def authenticate():
    auth_header = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_header}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return jsonify(response.json()), response.status_code

@app.route('/currently-playing', methods=['GET'])
def currently_playing():
    access_token = request.headers.get('Authorization').split(' ')[1]
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(port=5000)
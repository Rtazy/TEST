# app.py

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

#  Facebook App credentials
FACEBOOK_APP_ID = 'your_app_id'
FACEBOOK_APP_SECRET = 'your_app_secret'
FACEBOOK_REDIRECT_URI = 'your_redirect_uri'
FACEBOOK_ACCESS_TOKEN = 'your_access_token'  # Obtain this token after user authentication

# Facebook API endpoint
FACEBOOK_POST_URL = 'https://graph.facebook.com/v12.0/me/feed'

@app.route('/', methods=['GET'])
def index():
    return render_template('automate_post.html')

@app.route('/post', methods=['POST'])
def automate_post():
    post_content = request.form.get('post_content')
    post_on_facebook(post_content)
    return "Facebook post automated successfully!"

def post_on_facebook(content):
    params = {
        'message': content,
        'access_token': FACEBOOK_ACCESS_TOKEN,
    }

    response = requests.post(FACEBOOK_POST_URL, params=params)

    if response.status_code == 200:
        print('Facebook post successful!')
    else:
        print(f'Error posting on Facebook. Status Code: {response.status_code}, Message: {response.text}')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import openai
import tweepy

app = Flask(__name__)

# Set API key
openai.api_key = 'YOUR_API_KEY'
consumer_key = 'your_twitter_consumer_key'
consumer_secret = 'your_twitter_consumer_secret'
access_token = 'your_twitter_access_token'
access_token_secret = 'your_twitter_access_token_secret'

# Configure Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)


def generate_special_needs_post():
    #
    prompt = (
        "Our foundation, Al Nour, is dedicated to supporting individuals with special needs. "
        "We believe in creating a more inclusive and supportive community for everyone. "
        "Our mission is to integrating people with special needs into society and guarantee their needs. "
        "Through our various programs and activities. "
        "We have witnessed incredible stories of resilience and growth, showcasing the positive impact "
         "our foundation has on the lives of those we serve. Join us in making a difference for people with "
         "special needs and help us build a world where everyone is valued and included. "
         "Your financial support is crucial to our mission. With your generous donations"
        "special needs and help us build a world where everyone is valued and included."
    )

    # OpenAI  generates text based on the prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=300
    )

    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('Post.html')

@app.route('/generate_post', methods=['POST'])
def generate_post():
    generated_post = generate_special_needs_post()
    return render_template('Post.html', post=generated_post)

@app.route('/post_to_twitter', methods=['POST'])
def post_to_twitter():
    generated_post = request.form['generated_post']

    # Post to Twitter
    try:
        twitter_api.update_status(status=generated_post)
        return redirect(url_for('home'))
    except tweepy.TweepError as e:
        return f"Error posting to Twitter: {e}"

if __name__ == '__main__':
    app.run(debug=True)

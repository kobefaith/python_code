from flask import Flask,url_for,session,request,jsonify
from flask_oauthlib.client import OAuth

CLIENT_ID = 'juj45uwafY1uJGFAaJ6EKF6XpswZh7xCxqQWSd8F'
CLIENT_SECRET = 'CJNjiXdtcy3AeE5EaHr1BHGGQdUVAexCwCkIELQz7rSdrfX4VA'

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
oauth = OAuth(app)

remote = oauth.remote_app(
'remote',
consumer_key=CLIENT_ID,
consumer_secret=CLIENT_SECRET,
request_token_params={'scope':'email'},
base_url='http://127.0.0.1:5000/api/',
request_token_url=None,
access_token_url='http://127.0.0.1:5000/oauth/token',
authorize_url='http://127.0.0.1:5000/oauth/authorize'
)



























































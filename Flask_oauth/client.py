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
@app.route('/')
def index():
   if 'remote_oauth' in session:
        resp = remote.get('me')
        return jsonify(resp.data)
   next_url = request.args.get('next') or request.referrer or None
   return remote.authorize(
        callback=url_for('authorized',next=next_url,_external=True)
   )
@app.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied :reason=%s error=%s' %(
            request.args['error_reason'],
            request.args['error_description']
        )
    print resp
    session['remote_oauth'] = (resp['access_token'],'')
    return jsonify(oauth_token=resp['access_token'])
@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')

if __name__=='__main__':
    import os
    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(host='localhost',port=8000)


    
@app.route('/client/login',methods=['POST','GET'])
def client_login():
    uri = 'http://localhost:5000/oauth?response_type=code&client_id=%s&redirect_uri=%s' %(client_id,redirect_uri) 
    return redirect(uri)
@app.route('/client/passport',methods=['POST','GET']) 
def client_passport():
    code = request.args.get('code')
    uri = 'http://localhost:5000/oauth?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s' %(code,redirect_uri,client_id) 
    return redirect(uri)    





















































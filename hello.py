import re
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__, static_url_path='')

DROPBOX_APP_KEY = 'nueis1g9j2m3rdg'
DROPBOX_APP_SECRET = 'mhccn9ajway3gk7'

@app.route('/')
def hello_world():
    return app.send_static_file("index.html")
    if not 'access_token' in session:
        return redirect(url_for('dropbox_auth_start'))
    return 'Authenticated.'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        image_string = re.search(r'base64,(.*)', request.data).group(1)

        output = open('pics/' + str(uuid.uuid4()) + '.png', 'wb')
        output.write(image_string.decode('base64'))
        output.close()
    except Exception as e:
        pass

    return jsonify(success=True)

if __name__ == '__main__':
    app.debug = True
    app.run()
@app.route('/dropbox-auth-start')
def dropbox_auth_start():
    return redirect(get_auth_flow().start())

@app.route('/dropbox-auth-finish')
def dropbox_auth_finish():
    try:
        access_token, user_id, url_state = get_auth_flow().finish(request.args)
    except:
        abort(400)
    else:
        session['access_token'] = access_token
    return redirect(url_for('home'))

def get_auth_flow():
    redirect_uri = url_for('dropbox_auth_finish', _external=True)
    return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, redirect_uri,
                             session, 'dropbox-auth-csrf-token')

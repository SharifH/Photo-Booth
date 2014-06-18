import dropbox
import re
import uuid
from flask import Flask, request, jsonify, session, redirect, url_for, abort

from dropbox.client import DropboxClient, DropboxOAuth2Flow, DropboxOAuth2FlowNoRedirect
from dropbox.rest import ErrorResponse, RESTSocketError
from dropbox.datastore import DatastoreError, DatastoreManager, Date, Bytes

app = Flask(__name__, static_url_path='')

DROPBOX_APP_KEY = 'nueis1g9j2m3rdg'
DROPBOX_APP_SECRET = 'mhccn9ajway3gk7'

@app.route('/')
def hello_world():
    if not 'access_token' in session:
        return redirect(url_for('dropbox_auth_start'))
    return app.send_static_file("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        client = dropbox.client.DropboxClient(session['access_token'])

        image_string = re.search(r'base64,(.*)', request.data).group(1)

        file_name = 'pics/' + str(uuid.uuid4()) + '.png'

        output = open(file_name, 'wb')
        output.write(image_string.decode('base64'))
        output.close()

        response = client.put_file(file_name, f)
    except Exception as e:
        print e
        pass

    return jsonify(success=True)

@app.route('/dropbox-auth-start')
def dropbox_auth_start():
    return redirect(get_auth_flow().start())

@app.route('/dropbox-auth-finish')
def dropbox_auth_finish():
    try:
        access_token, user_id, url_state = get_auth_flow().finish(request.args)
    except Exception as e:
        print e
        abort(400)
    else:
        session['access_token'] = access_token
    return app.send_static_file("index.html")
    # return redirect(url_for('home'))

def get_auth_flow():
    redirect_uri = url_for('dropbox_auth_finish', _external=True)
    return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, redirect_uri,
                             session, 'dropbox-auth-csrf-token')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()

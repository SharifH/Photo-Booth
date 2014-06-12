import re
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__, static_url_path='')


@app.route('/')
def hello_world():
    return app.send_static_file("index.html")

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

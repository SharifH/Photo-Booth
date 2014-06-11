from flask import Flask, request
app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    return app.send_static_file("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
  print request.files

if __name__ == '__main__':
    app.debug = True
    app.run()
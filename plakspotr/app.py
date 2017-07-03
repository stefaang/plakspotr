from flask import Flask, current_app, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/lgf')
def take_pic():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pic():
    request.form['data']
    return 'OK'

if __name__ == "__main__":
    app.run()



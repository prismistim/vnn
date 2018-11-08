from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    html = render_template('index.html')
    return html

if __name__ == "__main__":
    app.run(host="192.168.13.117", port=5880)
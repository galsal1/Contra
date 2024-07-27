from flask import Flask

app = Flask(__name__)

@app.route('/page1')
def page1():
    with open("website/page1.html") as f:
        return f.read()

@app.route('/page2')
def page2():
    with open("website/page2.html") as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True, port=80)

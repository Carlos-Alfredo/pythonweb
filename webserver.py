import flask
app = flask.Flask(__name__)

@app.route('/')
def hello_world():
   print('Hello World')

if __name__ == '__main__':
   print('Hello World')
   app.run(host="0.0.0.0", port=80)

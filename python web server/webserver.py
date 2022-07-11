from flask import Flask, render_template, request
import io
import json
import logging
from PIL import Image
from pymongo import MongoClient
import base64

mongodbIp='54.221.150.139'

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient('mongodb://{}:27017/'.format(mongodbIp))

# Set database
#db = client.camera_images
db = client.test_database
users = db.users

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/showImage/', methods = ['POST','GET'])
def showImage():
	if request.method == 'GET':
		return f"The URL /showImage is accessed directly. Try going to '/index' to submit form"
	if request.method == 'POST':
		data = request.form
		image = users.find_one({'cameraId':data['Camera_Id']})
		img_buffer=io.BytesIO(image['data'])
		img_buffer.seek(0)
		image_memory = base64.b64encode(img_buffer.getvalue())
		return render_template('showImage.html', camera_image = image_memory.decode('utf-8'))

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=80)
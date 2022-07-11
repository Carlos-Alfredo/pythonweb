from flask import Flask, render_template, request, session, redirect
import io
import os
import json
import logging
from pymongo import MongoClient
import base64
import boto3

def get_mongoIP():
	client=boto3.client('ec2',
	region_name= "us-east-1",
	aws_access_key_id=os.environ.get('aws_access_key_id'),
	aws_secret_access_key=os.environ.get('aws_secret_access_key')
	)
	reservations = client.describe_instances(InstanceIds=['i-00e60cdceba35d872']).get("Reservations")
	for reservation in reservations:
		for instance in reservation['Instances']:
			return(instance.get("PublicIpAddress"))

mongodbIp=get_mongoIP()

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient('mongodb://{}:27017/'.format(mongodbIp))

# Set database
#db = client.camera_images
db = client.cameraImage
users = db.users

app = Flask(__name__)
app.secret_key='123'

@app.route("/")
def start():
	return render_template('index.html')

@app.route('/showImage/', methods = ['POST','GET'])
def showImage():
	if request.method == 'GET':
		return f"The URL /showImage is accessed directly. Try going to '/index' to submit form"
	if request.method == 'POST':
		data = request.form
		session['Camera_Id']=data['Camera_Id']
		results = users.find({'cameraId':session['Camera_Id']}).limit(1).sort('timestamp',-1)
		for x in results:
			image=x
		img_buffer=io.BytesIO(image['data'])
		img_buffer.seek(0)
		image_memory = base64.b64encode(img_buffer.getvalue())
		return render_template('showImage.html', camera_image = image_memory.decode('utf-8'))

@app.route('/showImage/updateImage/')
def redirectUpImg1():
	return redirect('/updateImage/')

@app.route('/updateImage/updateImage/')
def redirectUpImg2():
	return redirect('/updateImage/')

@app.route('/showImage/index/')
def redirectIndex1():
	return redirect('/')

@app.route('/updateImage/index/')
def redirectIndex2():
	return redirect('/')

@app.route('/updateImage/')
def updateImage():
	results = users.find({'cameraId':session['Camera_Id']}).limit(1).sort('timestamp',-1)
	for x in results:
		image=x
	img_buffer=io.BytesIO(image['data'])
	img_buffer.seek(0)
	image_memory = base64.b64encode(img_buffer.getvalue())
	return render_template('showImage.html', camera_image = image_memory.decode('utf-8'))

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=80)

import logging
import json
import io
import os
import random
from pymongo import MongoClient
from PIL import Image
import boto3

def get_timestamp():
	client=boto3.client('lambda',
	region_name= "us-east-1",
    aws_access_key_id="AKIAV5MQB4Y6QUV5XP6W",
    aws_secret_access_key="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")
	payload = {"":""}
	result = client.invoke(
		FunctionName='getTime',
		InvocationType='RequestResponse',
		Payload=json.dumps(payload)
		)
	response = json.loads(result['Payload'].read())
	timestamp = json.loads(response['body'])
	return timestamp

def get_mongoIP():
	client=boto3.client('ec2',
	region_name= "us-east-1",
    aws_access_key_id="AKIAV5MQB4Y6QUV5XP6W",
    aws_secret_access_key="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")
	reservations = client.describe_instances(InstanceIds=['i-00e60cdceba35d872']).get("Reservations")
	for reservation in reservations:
		for instance in reservation['Instances']:
			return(instance.get("PublicIpAddress"))

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
mongodbIp=get_mongoIP()
client = MongoClient('mongodb://{}:27017/'.format(mongodbIp))

# Set database
db = client.cameraImage
users = db.users

def sendImage():
	#Get image
	cameraId='1'
	folder="C:/Users/carlo/Documents/Distribuidos/Camera1"
	filename = random.choice(os.listdir(folder))
	file=os.path.join(folder,filename)
	im = Image.open(file)
	image_bytes = io.BytesIO()
	im.save(image_bytes, format='JPEG')
	#Get timestamp
	timestamp = get_timestamp()
	image1 = {
	    'data': image_bytes.getvalue(),
	    'cameraId': cameraId,
	    'timestamp':timestamp
	}

	#Inserir
	image_id1 = users.insert_one(image1).inserted_id

	#Get image
	cameraId='2'
	folder="C:/Users/carlo/Documents/Distribuidos/Camera2"
	filename = random.choice(os.listdir(folder))
	file=os.path.join(folder,filename)
	im = Image.open(file)
	image_bytes = io.BytesIO()
	im.save(image_bytes, format='JPEG')
	#Get timestamp
	timestamp = get_timestamp()
	image2 = {
	    'data': image_bytes.getvalue(),
	    'cameraId': cameraId,
	    'timestamp':timestamp
	}

	#Inserir
	image_id2 = users.insert_one(image2).inserted_id

	#Get image
	cameraId='3'
	folder="C:/Users/carlo/Documents/Distribuidos/Camera3"
	filename = random.choice(os.listdir(folder))
	file=os.path.join(folder,filename)
	im = Image.open(file)
	image_bytes = io.BytesIO()
	im.save(image_bytes, format='JPEG')
	#Get timestamp
	timestamp = get_timestamp()
	image3 = {
	    'data': image_bytes.getvalue(),
	    'cameraId': cameraId,
	    'timestamp':timestamp
	}

	#Inserir
	image_id3 = users.insert_one(image3).inserted_id

	#Get image
	cameraId='4'
	folder="C:/Users/carlo/Documents/Distribuidos/Camera4"
	filename = random.choice(os.listdir(folder))
	file=os.path.join(folder,filename)
	im = Image.open(file)
	image_bytes = io.BytesIO()
	im.save(image_bytes, format='JPEG')
	#Get timestamp
	timestamp = get_timestamp()
	image4 = {
	    'data': image_bytes.getvalue(),
	    'cameraId': cameraId,
	    'timestamp':timestamp
	}

	#Inserir
	image_id4 = users.insert_one(image4).inserted_id

sendImage()
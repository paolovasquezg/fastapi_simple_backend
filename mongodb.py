# from pymongo import MongoClient

# uri = 'mongodb://localhost:27017'

# client = MongoClient(uri)
# db = client['test']
# productos = db['productos']
# productos_duenio = db["productos_duenio"]

import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")  # Change region if needed

# Connect to DynamoDB tables (equivalent to MongoDB collections)
productos = dynamodb.Table('productos')
productos_duenio = dynamodb.Table('productos_duenio')
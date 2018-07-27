import boto3
from botocore.client import Config
import random
import string
from decouple import config

def generateNewFileName(filename):
    splitfilename = filename.rpartition('.')
    filename = splitfilename[0]
    filecode = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    filetype = splitfilename[len(splitfilename) -1]
    newfilename = filename + "-" + filecode + "." + filetype
    return newfilename

def sendImageToS3(this_img):
    ACCESS_KEY_ID = 'AKIAIW5SNI7OPVDFYQYA'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'wedding-photo-gallery-assets'

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(BUCKET_NAME).put_object(Key=this_img.name, Body=this_img, ContentType='image/*', ContentEncoding='base64')

    return "https://s3-us-west-1.amazonaws.com/wedding-photo-gallery-assets/" + this_img.name
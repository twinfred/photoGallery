import boto3
from botocore.client import Config
import random
import string
from decouple import config
from PIL import Image
import re

def generateNewFileName(filename):
    splitfilename = filename.rpartition('.')
    filename = splitfilename[0]
    filename = re.sub('[^0-9a-zA-Z]+', '-', filename)
    filecode = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    filetype = splitfilename[len(splitfilename) -1]
    newfilename = "{}-{}.{}".format(filename, filecode, filetype)
    return newfilename

def sendImageToS3(this_img):
    print(this_img)
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'wedding-photos-gallery'

    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=this_img.name, Body=this_img, ContentType='image/*')

    return "https://s3.us-east-2.amazonaws.com/" + AWS_STORAGE_BUCKET_NAME + "/" + this_img.name
import boto3
from botocore.client import Config
import random
import string
from decouple import config
from PIL import Image

def generateNewFileName(filename):
    splitfilename = filename.rpartition('.')
    filename = splitfilename[0]
    filename = filename.replace(" ", "-")
    filecode = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    filetype = splitfilename[len(splitfilename) -1]
    newfilename = filename + "-" + filecode + "." + filetype
    return newfilename

def sendImageToS3(this_img):
    print(this_img)
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'wedding-photo-gallery-assets'

    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=this_img.name, Body=this_img, ContentType='image/*')

    return "https://s3-us-west-1.amazonaws.com/wedding-photo-gallery-assets/" + this_img.name
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from mongoengine import Document, fields, connect
from photoGallery.settings import DBNAME
import re
import bcrypt
from .s3image import sendImageToS3, generateNewFileName

connect(DBNAME)

class GalleryPhoto(Document):
    photo = fields.StringField()
    liked_by = fields.ListField(fields.StringField())
    approved = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager():

    # Registration Validator
    def reg_validator(self, postData):
        errors = {}
        email = (postData['email']).lower()
        if len(User.objects(email=email)) > 0:
            errors['email'] = "Your email already exists within our system."
            return errors
        if len(postData['fname']) < 1:
            errors['fname'] = "A first name is required."
        if len(postData['lname']) < 1:
            errors['lname'] = "A last name is required."
        if len(postData['email']) < 1:
            errors['email'] = "An email is required."
        elif not EMAIL_REGEX.match(email):
            errors['email'] = "Your email is not the correct format."
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters long."
        elif postData['password'] != postData['pass_conf']:
            errors['password'] = "Your passwords don't match."
        return errors
    
    # Create New User
    def create_user(self, postData):
        fname = postData['fname']
        lname = postData['lname']
        email = postData['email'].lower()
        password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        if len(User.objects) == 0:
            user_level = 9
        else:
            user_level = 1
        new_user = User(fname=fname, lname=lname, email=email, password=password, user_level=user_level)
        new_user.save()
        return new_user

    # Login Validator
    def login_validator(self, postData):
        errors = {}
        email = (postData['email']).lower()
        user = User.objects(email = email).first()
        if user:
            User.objects(email = email).first()
        else:
            errors['login'] = "The email or password you entered was incorrect."
            return errors
        password = bcrypt.checkpw(postData['password'].encode(), user.password.encode())
        if password == False:
            errors['password'] = "The email or password you entered was incorrect."
        if errors:
            return errors
    
    # Login User
    def login_user(self, postData):
        email = (postData['email']).lower()
        user = User.objects(email=email)[0]
        return user
    
    # Add Photo to User
    def add_photo(self, postData, fileData, email):
        fileData['wedding_image'].name = generateNewFileName(fileData['wedding_image'].name)
        photo_uploaded = sendImageToS3(fileData['wedding_image'])
        user = User.objects(email=email)[0]
        if user.user_level == 9:
            new_photo = GalleryPhoto(photo=photo_uploaded, approved=True)
        else:
            new_photo = GalleryPhoto(photo=photo_uploaded)
        new_photo.save()
        user.update(add_to_set__photos=new_photo)
        return

    # Like a Photo
    def like_photo(self, image_id, email):
        photo = GalleryPhoto.objects(id=image_id)
        user = User.objects(email=email)[0]
        photo.update(add_to_set__liked_by=user.id)
        return

class User(Document):
    fname = fields.StringField(required=True, min_length=1)
    lname = fields.StringField(required=True, min_length=1)
    email = fields.StringField(required=True, min_length=1)
    password = fields.StringField(required=True)
    user_level = fields.IntField(default=1)
    photos = fields.ListField(fields.ReferenceField(GalleryPhoto))
    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)
    user_manager = UserManager()
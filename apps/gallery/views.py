# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import User, GalleryPhoto, UserManager
from django.contrib import messages
from django.template import RequestContext
import bcrypt
# from bson import json_util

# Admin
def admin(request):
    # User must be logged in
    if not 'email' in request.session:
        return redirect('/')
    else:
        user = User.objects(email = request.session['email'])[0]
        # Is user an admin (level 9)?
        if user.user_level != 9:
            return redirect('/')
        else:
            print('awesome')
            context = {
                'images': GalleryPhoto.objects(approved=True).order_by('-created_at'),
                'pending_images': GalleryPhoto.objects(approved=False),
            }
            return render(request, 'gallery/admin.html', context)

# User-Facing Pages
def index(request):
    if request.GET != {}:
        if request.GET['sort'] == 'likes':
            photos = GalleryPhoto.objects(approved=True)
            print photos
            for photo in photos:
                photo.like_count = len(photo['liked_by'])
            context = {
                'images': photos.order_by('-like_count')
            }
        else:
            context = {
                'images': GalleryPhoto.objects(approved=True).order_by('-created_at')
            }
    else:
        context = {
                'images': GalleryPhoto.objects(approved=True).order_by('-created_at')
            }
    if 'email' in request.session:
        context['this_user'] = User.objects.get(email = request.session['email'])
    return render(request, 'gallery/index.html', context)

# Login/Reg
def register(request):
    if request.method == 'GET':
        # Is user logged in already?
        if 'email' in request.session:
            return redirect('/')
        else:
            return render(request, 'gallery/register.html')
    if request.method == 'POST':
        errors = User.user_manager.reg_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/register')
        else:
            new_user = User.user_manager.create_user(request.POST)
            request.session['email'] = new_user.email
            return redirect('/')

def login(request):
    if request.method == 'GET':
        # Is user logged in already?
        if 'email' in request.session:
            return redirect('/')
        else:
            return render(request, 'gallery/login.html')
    if request.method == 'POST':
        errors = User.user_manager.login_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/login')
        else:
            user = User.user_manager.login_user(request.POST)
            request.session['email'] = user.email
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

# Images
def images(request, image_id=''):
    if not 'email' in request.session:
        return redirect('/register')
    if request.method == 'GET':
        return render(request, 'gallery/add_img.html')
    if request.method == 'POST' and image_id == '':
        email = request.session['email']
        User.user_manager.add_photo(request.POST, request.FILES, email)
        user = User.objects(email=email)[0]
        if user.user_level == 9:
            messages.success(request, "Your image was added.")
        else:
            messages.success(request, "Your image was submitted and will be available once it has been approved.")
        return redirect('/images')

def like(request, image_id=''):
    if not 'email' in request.session:
        return redirect('/register')
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        email = request.session['email']
        User.user_manager.like_photo(image_id, email)
        return redirect('/')
    else:
        print('doh')
        return redirect('/')

def approve(request, image_id=''):
    if not 'email' in request.session:
        return redirect('/register')
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        email = request.session['email']
        user = User.objects(email=email)[0]
        if user.user_level != 9:
            return redirect('/')
        else:
            User.user_manager.approve_photo(image_id)
            return redirect('/admin')
    else:
        print('doh!')
        return redirect('/')


# Catch-All
def home(request):
    return redirect('/')
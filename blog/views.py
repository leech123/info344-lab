from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from blog.models import Post 
from blog.serializers import PostSerializer
from django.contrib.auth.decorators import login_required #authenication helper
import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import os
import re

# login_required() decorator 
# this view requires an authenticated user 
c = S3Connection('','')

@login_required(login_url='accounts/login/')
def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url='accounts/login/')
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)

			link = urllib.request.urlopen(post.original_url)
			post.final_url = link.geturl()
			post.http_status = link.getcode()
			r = requests.get(post.final_url)

			#BeautifulSoup to scrape title		
			soup = BeautifulSoup(r.text, "html.parser")
			post.title = soup.title.string

			#Webcapture using phantomjs
			driver = webdriver.PhantomJS()
			driver.set_window_size(1024, 768)
			driver.get(post.final_url)
			regex = re.compile('[^a-zA-Z]')
			simpletitle = regex.sub('', post.title)
			driver.save_screenshot('/home/ubuntu/tmp/' + simpletitle + '.png')

			#uploading image to s3 using boto
			b = c.get_bucket('leech-bucket-lab3')
			k = Key(b)
			k.key = simpletitle + '.png'
			k.set_contents_from_filename('/home/ubuntu/tmp/' + simpletitle+ '.png')
			k.make_public()
			post.webcapture = 'https://s3.amazonaws.com/leech-bucket-lab3/' + simpletitle + '.png'
			os.remove('/home/ubuntu/tmp/' + simpletitle + '.png')
			
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm()

	return render(request, 'blog/post_edit.html' , {'form': form})

@login_required(login_url='accounts/login/')
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

@login_required(login_url='accounts/login/')
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='accounts/login/')
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)

	#deletes image file from s3 using boto
	regex = re.compile('[^a-zA-Z]')
	simpletitle = regex.sub('', post.title)
	b = c.get_bucket('leech-bucket-lab3')
	k = Key(b)
	k.key = simpletitle + '.png'
	k.delete()

	post.delete()
	return redirect('blog.views.post_list')

@login_required(login_url='accounts/login/')
def post_recapture(request, pk):
	post = get_object_or_404(Post, pk=pk)

	#Webcapture using phantomjs
	driver = webdriver.PhantomJS()
	driver.set_window_size(1024, 768)
	driver.get(post.final_url)
	regex = re.compile('[^a-zA-Z]')
	simpletitle = regex.sub('', post.title)
	driver.save_screenshot('/home/ubuntu/tmp/' + simpletitle + '.png')

	#uploading image to s3 using boto
	b = c.get_bucket('leech-bucket-lab3')
	k = Key(b)
	k.key = simpletitle + '.png'
	k.delete()

	k = Key(b)
	k.key = simpletitle + '.png'
	k.set_contents_from_filename('/home/ubuntu/tmp/' + simpletitle + '.png')
	k.make_public()
	post.webcapture = 'https://s3.amazonaws.com/leech-bucket-lab3/' + simpletitle + '.png'

	os.remove('/home/ubuntu/tmp/' + simpletitle + '.png')
	
	post.save()
	return redirect('blog.views.post_detail', pk=post.pk)



@login_required(login_url='accounts/login/')
@api_view(['GET', 'POST'])
def post_list_rest_api(request, format=None):
	'''
	List all urls, or create a new url
	'''
	if request.method == 'GET':
		post = Post.objects.all()
		serializer = PostSerializer(post, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='accounts/login/')
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail_rest_api(request, pk, format=None):
	'''
	Retrieve, update or delete url instance
	'''
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = PostSerializer(post)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		post.delete()
		return Response(status=status.HTP_204_NO_CONTENT)

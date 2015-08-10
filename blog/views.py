from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import urllib.request
from bs4 import BeautifulSoup

# Create your views here.
def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html' , {'form': form})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	link = urllib.request.urlopen(post.original_url)
	post.final_url = link.geturl()

	content = urllib.request.urlopen(post.final_url).read()
	soup = BeautifulSoup(content)
	post.title = soup.title.string
	

	post.html_status = link.getcode()
	return render(request, 'blog/post_detail.html', {'post': post})

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

def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return HttpeResponse('deleted')


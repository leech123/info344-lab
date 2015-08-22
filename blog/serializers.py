from django.forms import widgets 
from rest_framework import serializers 
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('original_url', 'final_url', 'http_status', 'title', 'webcapture',)
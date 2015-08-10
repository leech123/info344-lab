from django.db import models

# Create your models here.


class Post(models.Model):
	original_url = models.URLField()
	final_url = ''
	http_status = ''
	title = ''

	def publish(self):
		self.save()

	def __str__(self):
		return self.original_url
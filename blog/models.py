from django.db import models

# Create your models here.


class Post(models.Model):
	original_url = models.URLField()
	final_url = models.URLField(default='DEFAULT VALUE')
	http_status = models.CharField(max_length=200, default='DEFAULT VALUE')
	title = models.CharField(max_length=200, default='DEFAULT VALUE')
	webcapture = models.URLField(default='DEFAULT VALUE')

	def publish(self):
		self.save()

	def __str__(self):
		return self.original_url
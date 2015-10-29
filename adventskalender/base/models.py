from django.db import models

from django.core.urlresolvers import reverse

from google.appengine.api import images as gimages
from google.appengine.ext import blobstore

# Create your models here.

class Reward(models.Model):
	text = models.TextField(max_length=2000)
	key = models.CharField(max_length=64, unique=True)
	#file
	#foreign keys
	def __str__(self):
		return self.key

class Image(models.Model):
	image = models.ImageField(upload_to='uploads')
	blob_key = models.CharField(max_length=300)
	reward = models.ForeignKey(Reward)
	def serving_url(self):
		try:
			return gimages.get_serving_url(self.blob_key)
		except:
			return ""
	def content_type(self):
		try:
			return blobstore.BlobInfo.get(self.blob_key).content_type
		except:
			return ""
	def filename(self):
		try:
			return blobstore.BlobInfo.get(self.blob_key).filename
		except:
			return ""
	def download_url(self):
		try:
			return reverse('files', kwargs={'blob_key': self.blob_key})
		except:
			return ""

class Condition(models.Model):
	valid_from = models.DateTimeField(null=True, blank=True)
	valid_til = models.DateTimeField(null=True, blank=True)
	#foreign keys
	reward = models.ForeignKey(Reward)
	def __str__(self):
		return "from " + str(self.valid_from) + " to " + str(self.valid_til)

class Riddle(models.Model):
	question = models.TextField(max_length=2000)
	answer = models.TextField(max_length=2000)
	#file
	#foreign keys
	reward = models.ForeignKey(Reward)
	def __str__(self):
		return self.question[:30]

class Hint(models.Model):
	hint = models.TextField(max_length=2000)
	#foreign keys
	riddle = models.ForeignKey(Riddle)
	def __str__(self):
		return self.hint[:30]

class Choice(models.Model):
	text = models.TextField(max_length=2000)
	#foreign keys
	riddle = models.ForeignKey(Riddle)
	def __str__(self):
		return self.text[:30]

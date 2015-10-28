from django.db import models

from google.appengine.api import images as gimages

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
		print "blobkey: " + self.blob_key
		return gimages.get_serving_url(self.blob_key)

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

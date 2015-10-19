from django.db import models

# Create your models here.

class Reward(models.Model):
	text = models.CharField(max_length=200)
	key = models.CharField(max_length=64)
	#file
	#foreign keys

class Condition(models.Model):
	valid_from = models.DateTimeField(null=True, blank=True)
	valid_til = models.DateTimeField(null=True, blank=True)
	#foreign keys
	reward = models.ForeignKey(Reward)

class Riddle(models.Model):
	question = models.CharField(max_length=200)
	answer = models.CharField(max_length=200)
	#file
	#foreign keys
	reward = models.ForeignKey(Reward)

class Hint(models.Model):
	hint = models.CharField(max_length=200)
	#foreign keys
	riddle = models.ForeignKey(Riddle)

class Choice(models.Model):
	text = models.CharField(max_length=200)
	#foreign keys
	riddle = models.ForeignKey(Riddle)
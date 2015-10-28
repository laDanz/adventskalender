# coding=utf8
import cgi
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet


from base.models import Reward, Condition, Riddle, Image

from google.appengine.ext import blobstore
from google.appengine.api import images as gimages

def home(request):
	return render_to_response('home.html')

def reward(request, key):
	try:
		reward = Reward.objects.get(key=key)
	except Reward.DoesNotExist:
		return HttpResponse("Solch ein Rätsel gibt es nicht!")
	#are conditions met?
	current_time=timezone.now()
	#print current_time
	conditions = reward.condition_set.all()
	for condition in conditions:
		#print condition.valid_from
		#print condition.valid_til
		if (not condition.valid_from is None and current_time < condition.valid_from) or \
			(not condition.valid_til is None and current_time > condition.valid_til):
			return render_to_response('reward/condition_not_met.html', {'condition': condition})
	riddles = reward.riddle_set.order_by("pk")
	if riddles.count > 0:
		solved_all = True
		error_message = ""
		for riddle in riddles:
			riddle.tries = 0
			if str(riddle.pk)+"_tries" in request.POST.keys():
				riddle.tries = int(request.POST[str(riddle.pk)+"_tries"])
			answer_key = str(riddle.pk)+'_user_answer'
			if answer_key not in request.POST.keys():
				solved_all = False
				break
			user_answer = request.POST[answer_key]
			if riddle.answer != user_answer:
				solved_all = False
				error_message = "Fehler, versuchs nochmal!"
				riddle.tries+=1
		if not solved_all:
			return render_to_response('reward/detail.html', {'reward': reward, 'riddles':riddles, 'error_message':error_message}, context_instance=RequestContext(request))
	return render_to_response('reward/earned.html', {'reward': reward})

class RewardManageForm(ModelForm):
	class Meta:
		model = Reward
		fields = ('id', 'key', 'text')

class ImageManageForm(ModelForm):
	class Meta:
		model = Image

class ConditionManageForm(ModelForm):
	class Meta:
		model = Condition

class RiddleManageForm(ModelForm):
	class Meta:
		model = Riddle

def images(request, blob_key):
	serving_url = gimages.get_serving_url(blob_key)
	return render_to_response('debug/images.html', {'serving_url': serving_url, })

def get_blobinfo_from_post(request):
	request.META['wsgi.input'].seek(0)
	fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)
	value = fields["image"]
	blob_info=blobstore.parse_blob_info(value)
	if blob_info.size == 0:
		blob_info.delete()
		return None
	return blob_info

def upoadsuccess(request):
	blob_info = get_blobinfo_from_post(request)
	return render_to_response('debug/upoadsuccess.html', {'request': request, 'file':request.FILES['image'], 'binfo':blob_info, 'sbinfo':dir(blob_info) })

def manage_reward(request, key):
	image = Image()
	try:
		reward = Reward.objects.get(key=key)
		image = reward.image_set.all()
	except Reward.DoesNotExist:
		reward = Reward()
		reward.key = key
		
	if request.method == 'POST':
		form = RewardManageForm(instance=reward, data=request.POST)
		if form.is_valid():
			form.save()
			blob_info = get_blobinfo_from_post(request)
			if blob_info is not None:
				print "blobkey: " + str(blob_info.key())
				image = Image()
				image.blob_key = str(blob_info.key())
				image.reward = Reward.objects.get(key=key)
				image.save()
	else:
		form = RewardManageForm(instance=reward)
		
	if isinstance(image, QuerySet):
		image_forms = []
		if image.count()==0:
			image_forms = [ImageManageForm(instance=Image()), ]
		else:
			for i in image:
				image_forms.append(ImageManageForm(instance=i))
	else:
		image_forms = [ImageManageForm(instance=image), ]
	
	url = reverse('manage_reward', kwargs={'key': key})
	#url = '/success/'
	upload_url = blobstore.create_upload_url(url)
	return render_to_response('reward/manage.html', {'upload_url': upload_url, 'form': form, 'reward': reward, 'image_forms':image_forms}, context_instance=RequestContext(request))

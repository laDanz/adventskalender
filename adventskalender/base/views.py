# coding=utf8
import cgi

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from google.appengine.api import images as gimages
from google.appengine.ext import blobstore

from forms import RewardManageForm, ImageManageForm, ConditionManageForm, RiddleManageForm
from models import Reward, Condition, Riddle, Image


def home(request):
	return render_to_response('home.html')

def reward(request, key):
	try:
		reward = Reward.objects.get(key=key)
	except Reward.DoesNotExist:
		return render_to_response('reward/not_found.html')
	#are conditions met?
	current_time=timezone.now()
	#print current_time
	conditions = reward.condition_set.all()
	for condition in conditions:
		#print condition.valid_from
		#print condition.valid_til
		if (not condition.valid_from is None and current_time < condition.valid_from) or \
			(not condition.valid_til is None and current_time > condition.valid_til):
			return render_to_response('reward/condition_not_met.html', {'condition': condition, 'current_time':current_time})
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
				error_message = "Versuch es nochmal!"
				riddle.tries+=1
		if not solved_all:
			return render_to_response('reward/detail.html', {'reward': reward, 'riddles':riddles, 'error_message':error_message}, context_instance=RequestContext(request))
	return render_to_response('reward/earned.html', {'reward': reward})

def images(request, blob_key):
	serving_url = gimages.get_serving_url(blob_key)
	return render_to_response('debug/images.html', {'serving_url': serving_url, })


def read_in_chunks(file_object, chunk_size=1024):
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		yield data

def files(request, blob_key):
	binfo = blobstore.BlobInfo.get(blob_key)
	response = HttpResponse(content_type=binfo.content_type)
	response['Content-Disposition'] = 'attachment; filename=' + binfo.filename
	
	breader = binfo.open()
	for piece in read_in_chunks(breader):
		response.write(piece)
	breader.close()
	
	return response


def get_blobinfo_from_post(request):
	result = []
	request.META['wsgi.input'].seek(0)
	fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)
	values = []
	try:
		imagefields = fields["image"]
	except KeyError:
		return result
	if isinstance(imagefields, list):
		for i in imagefields:
			values.append( i )
	else:
		values.append( imagefields )
	for value in values:
		blob_info=blobstore.parse_blob_info(value)
		if blob_info.size == 0:
			blob_info.delete()
		else:
			result.append(blob_info)
	return result

def upoadsuccess(request):
	blob_info = get_blobinfo_from_post(request)
	return render_to_response('debug/upoadsuccess.html', {'request': request, 'file':request.FILES['image'], 'binfo':blob_info, 'sbinfo':dir(blob_info) })

@permission_required('add_reward')
def manage_reward(request, key):
	form = None
	riddle_form = None
	condition_form = None
	
	try:
		#loading existing reward
		reward = Reward.objects.get(key=key)
	except Reward.DoesNotExist:
		#creating new reward, initialize variables
		reward = Reward()
		reward.key = key
	
	riddle = reward.riddle_set.all()
	if riddle.count() == 0:
		riddle = Riddle()
	else:
		riddle = riddle[0]
	
	condition = reward.condition_set.all()
	if condition.count() == 0:
		condition = Condition()
	else:
		condition = condition[0]

	if request.method == 'POST':
		form = RewardManageForm(instance=reward, data=request.POST)
		if form.is_valid():
			reward = form.save()
			blob_infos = get_blobinfo_from_post(request)
			for blob_info in blob_infos:
				#print "blobkey: " + str(blob_info.key())
				image = Image()
				image.blob_key = str(blob_info.key())
				image.reward = reward
				image.save()
		riddle.reward = reward
		riddle_form = RiddleManageForm(instance=riddle, data=request.POST) 
		if riddle_form.is_valid():
			riddle_form.save()
		condition.reward = reward
		condition_form = ConditionManageForm(instance=condition, data=request.POST) 
		if condition_form.is_valid():
			condition_form.save()
		
	images = list(reward.image_set.all())
	images.append(Image())
	
	if form is None:
		form = RewardManageForm(instance=reward)
	
	image_forms = []
	for image in images:
		image_forms.append(ImageManageForm(instance=image))
	
	if riddle_form is None:
		riddle_form = RiddleManageForm(instance=riddle)
	
	if condition_form is None:
		condition_form = ConditionManageForm(instance=condition)

	url = reverse('manage_reward', kwargs={'key': key})
	upload_url = blobstore.create_upload_url(url)

	return render_to_response('reward/manage.html', {'upload_url': upload_url, 'form': form, 'reward': reward, 'image_forms':image_forms, 'riddle_form':riddle_form, 'condition_form':condition_form }, context_instance=RequestContext(request))

@permission_required('add_reward')
def list_rewards(request):
	context = {}
	rewards = Reward.objects.all().order_by("condition__valid_from")
	context["rewards"] = rewards
	return render_to_response('reward/list.html', context, context_instance=RequestContext(request))

@permission_required('add_reward')
def delete_reward(request, key):
	reward = Reward.objects.get(key=key)
	reward.delete()

	return redirect("list_rewards")














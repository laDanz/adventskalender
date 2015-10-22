# coding=utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone

from base.models import Reward, Condition, Riddle

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
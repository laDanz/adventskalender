from django import forms
from django.forms.models import inlineformset_factory

from base.models import *

class RewardManageForm(forms.ModelForm):
	class Meta:
		model = Reward
		fields = ('id', 'key', 'text')

################ Model Forms ################

class ImageManageForm(forms.ModelForm):
	class Meta:
		model = Image

class ConditionManageForm(forms.ModelForm):
	class Meta:
		model = Condition

class RiddleManageForm(forms.ModelForm):
	class Meta:
		model = Riddle


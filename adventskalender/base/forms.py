from django import forms
from models import Reward, Image, Condition, Riddle

class RewardManageForm(forms.ModelForm):
	class Meta:
		model = Reward
		fields = ('id', 'key', 'text')

################ Model Forms ################

class ImageManageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('image', )

class ConditionManageForm(forms.ModelForm):
	class Meta:
		model = Condition
		fields = ('valid_from', 'valid_til',)

class RiddleManageForm(forms.ModelForm):
	class Meta:
		model = Riddle
		fields = ('question', 'answer')


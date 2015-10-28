import os

from django.contrib import admin
from django.core.urlresolvers import reverse

from base.models import Riddle, Reward, Condition, Hint, Image

admin.site.register(Condition)
admin.site.register(Hint)
admin.site.register(Image)

class ConditionInline(admin.StackedInline):
	model = Condition
	extra = 0

class RiddleInline(admin.StackedInline):
	model = Riddle
	extra = 0

class HintInline(admin.StackedInline):
	model = Hint
	extra = 0

class RiddleAdmin(admin.ModelAdmin):
	inlines = [HintInline]

class RewardAdmin(admin.ModelAdmin):
	inlines = [ConditionInline, RiddleInline]

admin.site.register(Reward, RewardAdmin)

admin.site.register(Riddle, RiddleAdmin)

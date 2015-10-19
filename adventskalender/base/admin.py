from base.models import Riddle, Reward, Condition
from django.contrib import admin

admin.site.register(Riddle)
admin.site.register(Condition)


class ConditionInline(admin.StackedInline):
    model = Condition
    extra = 0

class RiddleInline(admin.StackedInline):
    model = Riddle
    extra = 0

class RewardAdmin(admin.ModelAdmin):
    inlines = [ConditionInline, RiddleInline]

admin.site.register(Reward, RewardAdmin)

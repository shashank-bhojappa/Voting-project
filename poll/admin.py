from django.contrib import admin
from poll.models import Poll, Voting_result
# Register your models here.
admin.site.register(Poll)
admin.site.register(Voting_result)

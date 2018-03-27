from django.contrib import admin
from .models import TempThresholdConfiguration, MobileNumber, PushoverUserKey
from solo.admin import SingletonModelAdmin


admin.site.register(MobileNumber)
admin.site.register(TempThresholdConfiguration, SingletonModelAdmin)
admin.site.register(PushoverUserKey)

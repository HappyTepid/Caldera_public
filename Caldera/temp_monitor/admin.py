from django.contrib import admin
from .models import TempThresholdConfiguration, MobileNumber, PushoverUserKey
from solo.admin import SingletonModelAdmin


admin.site.register(MobileNumber)
admin.site.register(TempThresholdConfiguration, SingletonModelAdmin)
admin.site.register(PushoverUserKey)
# get_solo will create the item if it does not already exist
config = TempThresholdConfiguration.get_solo()
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from solo.models import SingletonModel
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .sms import publicSMS
from .pushover import public_push
from .ses import public_send_email

# Create your models here.
class TemperatureReading(models.Model):
    date_time = models.DateTimeField()
    temperature = models.FloatField()

    def __str__(self):
        return str(self.temperature) + 'c @ ' + str(self.date_time)


class MobileNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = PhoneNumberField(default='+44')

    def __str__(self):
        return self.user.username + ' - ' + str(self.number)


class PushoverUserKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username + ' - ' + self.key


class TempThresholdConfiguration(SingletonModel):
    min_temp = models.FloatField(default=10.0)
    max_temp = models.FloatField(default=23.0)

    class Meta:
        verbose_name = "Thresholds"


class GlobalFlag(SingletonModel):
    alerts_sent = models.BooleanField(default=False)


@receiver(post_save, sender=TemperatureReading, dispatch_uid="evaluate_whether_to_alert")
def evaluate_alert(sender, instance, **kwargs):
    threshold = TempThresholdConfiguration.get_solo()
    global_flag = GlobalFlag.get_solo()
    if not threshold.min_temp < instance.temperature < threshold.max_temp and not global_flag.alerts_sent:
        numbers = [u.number for u in MobileNumber.objects.all()]
        pushover_keys = [u.key for u in PushoverUserKey.objects.all()]
        emails = [u.email for u in User.objects.all()]
        publicSMS(numbers, 'Alert: server room temperature is currently ' + str(instance.temperature) + ' degrees!')
        public_push(pushover_keys, 'Alert: server room temperature is currently ' + str(instance.temperature) + ' degrees!')
        public_send_email('Temperature alert!', 'Alert: server room temperature is currently ' + str(instance.temperature) + ' degrees!', emails)
        global_flag.alerts_sent = True
        global_flag.save()
    elif threshold.min_temp < instance.temperature < threshold.max_temp and global_flag.alerts_sent:
        numbers = [u.number for u in MobileNumber.objects.all()]
        pushover_keys = [u.key for u in PushoverUserKey.objects.all()]
        emails = [u.email for u in User.objects.all()]
        publicSMS(numbers, 'Server room temperature is back to normal range (' + str(instance.temperature) + ' degrees)')
        public_push(pushover_keys, 'Server room temperature is back to normal range (' + str(instance.temperature) + ' degrees)')
        public_send_email('Temperature normal', 'Server room temperature is back to normal range (' + str(instance.temperature) + ' degrees)', emails)
        global_flag.alerts_sent = False
        global_flag.save()

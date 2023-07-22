from django.db import models
# определяет правила для парсинга, создания и обработки электронных писем и их частей.
from email.policy import default
from app.account.models import User
from datetime import time, date, datetime
from app.utils import file_handling
from app.utils import choicess


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strtime('%H:%M:%S')

        is_open = None

        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, '%I:%M %p').time())
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open
  

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=choicess.DAYS)
    from_hour = models.CharField(choices=choicess.HOUR_OF_DAY_24, max_length=15, blank=True)
    to_hour = models.CharField(choices=choicess.HOUR_OF_DAY_24, max_length=15, blank=True)
    is_closed = models.BooleanField(default=False)


    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self) -> str:
        return self.get_day_display()

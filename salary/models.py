from django.db import models



class Workers(models.Model):
    CHOICES = (
        ('true', 'TRUE'),
        ('false', 'FALSE')
    )

    full_name = models.CharField(max_length=125)
    phone = models.CharField(max_length=12)
    age = models.IntegerField(default=0)
    job = models.CharField(max_length=125)
    birthday = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    salary = models.IntegerField(default=0)
    telegram_id = models.CharField(max_length=125)
    bons = models.IntegerField(default=0)
    fine = models.IntegerField(default=0)
    give = models.IntegerField(default=0)
    residue = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    start_work = models.ImageField(upload_to='start', blank=True, null=True)
    end_work = models.ImageField(upload_to='end', blank=True, null=True)
    data = models.DateField(auto_now=True, blank=True, null=True)
    type = models.CharField(max_length=12, blank=True, null=True)
    status = models.CharField(max_length=25, choices=CHOICES, default='true', blank=True, null=True)

    def __str__(self):
        return self.full_name




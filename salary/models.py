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
    clock_in = models.TimeField(blank=True, null=True)
    clock_out = models.TimeField(blank=True, null=True)
    month = models.CharField(blank=True, null=True, max_length=125)
    image = models.CharField(blank=True, null=True, max_length=125)
    type = models.CharField(max_length=12, blank=True, null=True)
    status = models.CharField(max_length=25, choices=CHOICES, default='true', blank=True, null=True)


    def __str__(self):
        return self.full_name


class Date(models.Model):
    worker = models.ForeignKey(Workers, on_delete=models.CASCADE, blank=True, null=True)
    clock_in = models.TimeField(blank=True, null=True)
    clock_out = models.TimeField(blank=True, null=True)
    work = models.CharField(blank=True, null=True, max_length=125)
    type_month = models.CharField(blank=True, null=True, max_length=125)
    month = models.CharField(blank=True, null=True, max_length=125)








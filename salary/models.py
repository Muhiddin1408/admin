from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=125)
    shop = models.CharField(max_length=125)
    salary = models.IntegerField(default=0)
    telegram_id = models.CharField(max_length=125)
    bons = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name



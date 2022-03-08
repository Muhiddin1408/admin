from django.contrib import admin
from .models import Workers, Date
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = Workers
        fields = "('full_name', 'salary', 'shop', 'telegram_id', 'bons')"


admin.site.register(Workers, UserAdmin)
admin.site.register(Date)


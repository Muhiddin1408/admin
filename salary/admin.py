from django.contrib import admin
from .models import Workers
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields': ('full_name', 'salary', 'shop', 'telegram_id','bons')
    #     }),)
    # fields = ('full_name', 'salary', 'shop', 'telegram_id', 'bons')

    class Meta:
        model = Workers
        fields = ('full_name', 'salary', 'shop', 'telegram_id', 'bons')


admin.site.register(Workers, UserAdmin)


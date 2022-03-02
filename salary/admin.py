from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields': ('full_name', 'salary', 'shop', 'telegram_id','bons')
    #     }),)
    # fields = ('full_name', 'salary', 'shop', 'telegram_id', 'bons')

    class Meta:
        model = User
        fields = ('full_name', 'salary', 'shop', 'telegram_id', 'bons')


admin.site.register(User, UserAdmin)


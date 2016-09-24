from django.contrib import admin

# Register your models here.
from taggserver.models import FlockUser


class FlockUserAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'user_id',
                    'user_token',
                    'created_at',
                    'updated_at')

admin.site.register(FlockUser, FlockUserAdmin)
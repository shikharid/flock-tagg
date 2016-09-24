from django.contrib import admin

# Register your models here.
from taggserver import models


class FlockUserAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'user_id',
                    'user_token',
                    'created_at',
                    'updated_at')

admin.site.register(models.FlockUser, FlockUserAdmin)
admin.site.register(models.Tag, admin.ModelAdmin)
admin.site.register(models.Content, admin.ModelAdmin)
admin.site.register(models.File, admin.ModelAdmin)
admin.site.register(models.Message, admin.ModelAdmin)
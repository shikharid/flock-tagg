from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_pgjson.fields import JsonField

# def get_file_path(testcase, name):
#     return os.path.join('test-case', '{0}.in'.format(testcase.id))


class Tag(models.Model):

    tag_value = models.CharField(null=False, blank=False, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FlockUser(models.Model):

    user_id = models.CharField(help_text="User ID", unique=True, max_length=256)
    user_token = models.CharField(help_text="x-flock-user-token", max_length=256)
    tags = models.ManyToManyField(Tag, help_text="Tags", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):

    MAX_MESSAGE_LENGTH = 10000

    message_content = models.CharField(null=True, blank=True, max_length=MAX_MESSAGE_LENGTH)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class File(models.Model):

    file_data = models.FileField()
    file_name = models.CharField(null=False, blank=False, max_length=256)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Content(models.Model):

    content_json = JsonField(help_text="Stores message content JSON")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Content)
def send_message(sender, instance, created, **kwargs):
    if created:
        created = created

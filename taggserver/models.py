import json
import os

import requests
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_pgjson.fields import JsonField


def get_file_path(instance, name):
    print 'Name: ', name
    return os.path.join('files', name)


class Tag(models.Model):
    tag_value = models.CharField(null=False, blank=False, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FlockUser(models.Model):
    user_id = models.CharField(help_text="User ID", unique=True, max_length=256)
    user_token = models.CharField(help_text="x-flock-user-token", max_length=256)
    tags = models.ManyToManyField(Tag, help_text="Tags", blank=True, related_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    MAX_MESSAGE_LENGTH = 10000

    message_content = models.CharField(null=True, blank=True, max_length=MAX_MESSAGE_LENGTH)
    tags = models.ManyToManyField(Tag, blank=True, related_name="message")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class File(models.Model):
    file_data = models.FileField(upload_to=get_file_path)
    tags = models.ManyToManyField(Tag, blank=True, related_name="file")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Content(models.Model):
    content_json = JsonField(help_text="Stores message content JSON")
    user = models.ForeignKey(FlockUser)
    to = models.CharField(null=False, blank=False, default='a', max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Content)
def send_message(sender, instance, created, **kwargs):
    if created:
        url = 'https://api.flock.co/v1/chat.sendMessage'
        payload = {
            "message": {
                "to": instance.to,
                "text": "Tagg Message",
                "attachments": [{
                    "id": "1",
                    "title": "Tagg Test",
                    "description": "Tagg Test",
                    "appId": "b7c39c29-bcdc-4bd0-94b9-6b58ed4c2917",
                    "color": "#0ABE51",
                    "views": {

                        "html": {"inline": "<b>Tagg Message! Click Open Button</b>", "width": 400, "height": 400}
                    }
                    ,
                    "buttons": [{
                        "name": "Open",
                        "icon": "icon 1 url",
                        "action": {"type": "openWidget", "desktopType": "modal", "mobileType": "modal",
                                   "url": "https://localhost:8080?cid={0}".format(instance.id)},
                        "id": "1"
                    }]
                }]
            }
        }
        headers = {
            'X-Flock-User-Token': instance.user.user_token
        }
        return requests.post(url, data=json.dumps(payload), headers=headers)

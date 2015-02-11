from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from user.models import User



class Notification(models.Model):
    """Table for all notifications."""
    date = models.DateTimeField(auto_now_add=True, db_index=True,
            auto_now=False,
            verbose_name="Creation date")
    title = models.TextField(null=True, blank=True,
            verbose_name="Title")
    read = models.BooleanField(default=False, db_index=True)
    receiver = models.ForeignKey(User, related_name="receiver", null=True)
    sender = models.ForeignKey(User, related_name="sender", null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

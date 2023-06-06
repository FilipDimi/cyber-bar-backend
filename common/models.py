from django.db import models
import uuid

class AbstractBaseModel(models.Model):
    """
    Template for the models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-datetime_created"]
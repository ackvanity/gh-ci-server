from django.db import models
import uuid


# Create your models here.
class Webhook(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True,
    )
    path = models.CharField()  # Path to local git repo
    script = models.CharField(blank=True)  # Path to CI script *relative* to repo
    secret = models.CharField()  # GitHub webhook key


class EnvVar(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    name = models.CharField()
    value = models.CharField()

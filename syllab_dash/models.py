from django.db import models

# Create your models here.


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')

    
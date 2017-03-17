from django.db import models

# Create your models here.
class WebInfo(models.Model):
    utilitiesinfo = models.TextField(max_length=5000)
    iouinfo = models.TextField(max_length=5000)
    choresinfo = models.TextField(max_length=5000)

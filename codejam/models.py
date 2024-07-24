# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta

class CommonSpace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    common_space = models.ForeignKey(CommonSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.end_time > self.start_time + timedelta(hours=4):
            raise ValidationError("end_time el tiempo maximo son 4 horas start_time")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.common_space.name} reservado por {self.user.username} desde {self.start_time} hasta {self.end_time}"
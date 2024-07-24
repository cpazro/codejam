# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta, time


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.name

class CommonSpace(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    description = models.TextField()
    capacity = models.IntegerField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.area} -- {self.category}'

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    common_space = models.ForeignKey(CommonSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.CharField(max_length=255)

    #reservar maximo 4 horas
    def save(self, *args, **kwargs):
        if self.end_time > self.start_time + timedelta(hours=4):
            raise ValidationError("end_time el tiempo maximo son 4 horas start_time")
        

    #solo se permiten reservas en los dias de semana
        if self.start_time.weekday() >= 5 or self.end_time.weekday() >= 5:
            raise ValidationError("Solo se puede reservar espacios de Lunes a Viernes.")

        if not (time(8, 0) <= self.start_time.time() <= time(20, 0)) or not (time(8, 0) <= self.end_time.time() <= time(20, 0)):
            raise ValidationError("Las reservas solo se pueden hacer entre las 8am y las 8pm.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.common_space.name} reservado por {self.user.username} desde {self.start_time} hasta {self.end_time}"
    

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"{self.common_space.name} reserved by {self.user.username} from {self.start_time} to {self.end_time}"

from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.TextField() #제품 이름
    location = models.TextField() #제품 위치

    def __str__(self):
        return self.name
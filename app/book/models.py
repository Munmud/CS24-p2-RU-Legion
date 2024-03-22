from django.db import models

# Create your models here.

class Book(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)  
    genre = models.CharField(max_length=255)  
    price = models.FloatField()  

    def __str__(self):
        return f"{self.title}"


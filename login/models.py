from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    pattern = models.CharField(max_length=255)
    total=models.IntegerField(default=0)
    currency=models.CharField(max_length=10, default='MRU')
    

    def __str__(self):
        return self.username
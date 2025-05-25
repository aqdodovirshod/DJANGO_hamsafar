from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    date = models.DateTimeField()
    seats = models.IntegerField(default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.start_location} to {self.end_location}"

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    date = models.DateTimeField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request by {self.user.username}"
    

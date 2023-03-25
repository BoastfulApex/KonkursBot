from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    phone = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.user_id


class Channel(models.Model):
    channel_id = models.CharField(max_length=20)
    link = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)


class WeekWinner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
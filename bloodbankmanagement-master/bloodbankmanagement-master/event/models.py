from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    time = models.DateTimeField()

    def __str__(self):
        return self.title

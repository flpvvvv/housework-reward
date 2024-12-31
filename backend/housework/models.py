from django.db import models

class HouseworkRecord(models.Model):
    contributor = models.CharField(max_length=100)
    record_time = models.DateTimeField(auto_now_add=True)
    scale = models.IntegerField(default=3)
    note = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True)

    def __str__(self):
        return f"{self.contributor} - {self.record_time}"
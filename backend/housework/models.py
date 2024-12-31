from django.db import models

class Contributor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class HouseworkRecord(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    record_time = models.DateTimeField(auto_now_add=True)
    scale = models.IntegerField(default=3)
    note = models.TextField(blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.contributor} - {self.record_time}"
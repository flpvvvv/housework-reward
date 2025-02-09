from django.db import models

class Contributor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class HouseworkRecord(models.Model):
    id = models.AutoField(primary_key=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    record_time = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=3)
    note = models.TextField(blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.contributor} - {self.record_time}"
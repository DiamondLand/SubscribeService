from django.db import models

class DataRecord(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

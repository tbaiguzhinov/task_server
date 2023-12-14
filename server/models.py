from django.db import models


class ErrorLog(models.Model):
    uuid = models.CharField(max_length=36, unique=True)
    error = models.TextField()
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.uuid} - {self.date_stamp}'

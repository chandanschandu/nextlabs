from django.db import models

class App(models.Model):
    app_icon = models.ImageField(upload_to='img')
    app_name = models.CharField(max_length=100)
    app_link = models.CharField(max_length=100)
    app_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.app_name

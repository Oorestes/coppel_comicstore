from django.db import models


class Character(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.URLField(max_length=250, null=False, blank=False)
    appearances = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name
    

class Comic(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False, blank=False)
    title = models.CharField(max_length=250, null=False, blank=False)
    image = models.URLField(max_length=250, null=False, blank=False)
    onsaleDate = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.title
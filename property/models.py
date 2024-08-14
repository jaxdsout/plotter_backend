from django.db import models


class Property(models.Model):
    MARKETS = [
        ('hou', 'Houston',),
        ('dfw', 'Dallas / Fort Worth'),
        ('atx', 'Austin')
    ]
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    website = models.CharField(max_length=250)
    market = models.CharField(max_length=100, choices=MARKETS, default='hou')
    neighborhood = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

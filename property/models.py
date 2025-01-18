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
    email = models.EmailField(max_length=250)

    def __str__(self):
        return self.name


class Commission(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='commissions')
    send = models.IntegerField(default=0, blank=True)
    escort = models.IntegerField(default=0, blank=True)
    flat_fee = models.IntegerField(default=0, blank=True)
    updated_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)



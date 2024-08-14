from django.db import models
from django.conf import settings
from property.models import Property
from user.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    trec = models.CharField(unique=True, max_length=6)
    website = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


class List(models.Model):
    date = models.DateTimeField(blank=True, auto_now_add=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='lists')

    def __str__(self):
        return str(self.client) + " List No. " + str(self.id)


class Option(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_number = models.CharField(max_length=20)
    layout = models.CharField(max_length=50)
    sq_ft = models.PositiveIntegerField()
    available = models.DateField(blank=True)
    notes = models.TextField('Notes / Specials', blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='options')
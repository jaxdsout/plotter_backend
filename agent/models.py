from django.db import models
from django.conf import settings
from property.models import Property
from user.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    trec = models.CharField(unique=True, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True)

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
    date = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='lists')
    uuid = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return str(self.client) + " List # " + str(self.id)


class Option(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit_number = models.CharField(max_length=20, null=True, blank=True)
    layout = models.CharField(max_length=50, null=True, blank=True)
    sq_ft = models.CharField(max_length=10, null=True, blank=True)
    available = models.DateField(blank=True, null=True)
    notes = models.TextField('Notes / Specials', blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='options')


class Deal(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rent = models.IntegerField()
    rate = models.IntegerField()
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    flat_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    move_date = models.DateField()
    unit_no = models.CharField(max_length=255)
    lease_term = models.CharField(max_length=255)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='deals')


class Card(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='cards')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cards')


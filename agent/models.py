from django.db import models
from django.conf import settings
from property.models import Property
from user.models import User
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string


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
    STATUS = [
        ('not', 'Not Invoiced',),
        ('pend', 'Pending'),
        ('over', 'Overdue'),
        ('paid', 'Paid')
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rent = models.IntegerField()
    rate = models.IntegerField(blank=True, null=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=25, choices=STATUS, default='not')
    flat_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    move_date = models.DateField()
    unit_no = models.CharField(max_length=255)
    lease_term = models.CharField(max_length=255)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='deals')
    deal_date = models.DateField(auto_now_add=True)
    invoice_date = models.DateField(blank=True, null=True)
    overdue_date = models.DateField(blank=True, null=True)
    lease_end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.move_date and self.lease_term:
            try:
                lease_term_months = int(self.lease_term)
                lease_end_date = self.move_date + timedelta(days=lease_term_months * 30)
                self.lease_end_date = lease_end_date
            except ValueError:
                pass

        super().save(*args, **kwargs)


class Card(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='cards')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cards')
    interested = models.CharField(max_length=255)
    move_by = models.CharField(max_length=255)




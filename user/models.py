from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Organization(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    orgname = models.CharField(max_length=200, null=True)
    orgemail = models.CharField(max_length=200, null=True)
    orgcontact = models.CharField(max_length=200, null=True)
    orgaddress = models.CharField(max_length=200, null=True)
    orglicense = models.CharField(max_length=200, null=True)
    orgdate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.orgname


class Event(models.Model):
    organization_name = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL)
    cover = models.ImageField(default="f.jpg", null=True, blank=False)
    event_title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    goal = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_title


class MoneyDonatorInfo(models.Model):
    event = models.ForeignKey(
        Event, null=True, on_delete=models.SET_NULL, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=264, blank=True)
    email = models.CharField(max_length=264, blank=True)
    contact = models.CharField(max_length=264, blank=True)
    opinion = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

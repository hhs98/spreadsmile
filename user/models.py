from django.db import models

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    license_no = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    organization = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_title

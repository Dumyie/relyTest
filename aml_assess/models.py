import re

from django.db import models


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=False)
    monthly_income = models.CharField(max_length=255)

    def full_name(self):
        name = self.first_name + "" + self.last_name
        full_name = re.sub('\W+', '', name).lower()
        # print(full_name)
        return full_name


class Application(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    sanctioned = models.BooleanField(null=True)
    pep = models.BooleanField(null=True)


class Sanction(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=False)

    def full_name(self):
        name = self.first_name + "" + self.last_name
        full_name = re.sub('\W+', '', name).lower()
        # print(full_name)
        return full_name


class PEP(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=False)

    def full_name(self):
        name = self.first_name + "" + self.last_name
        full_name = re.sub('\W+', '', name).lower()
        # print(full_name)
        return full_name


class PotentialMatch(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    check = models.CharField(max_length=255)
    id_match = models.IntegerField()
    match = models.BooleanField(default=True)

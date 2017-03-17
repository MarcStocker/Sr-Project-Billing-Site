from django.db import models

# Create your models here.

class Roommate(models.Model):
    name            = models.CharField(max_length=20)
    amountowed      = models.CharField(max_length=20)
    amountpaid      = models.CharField(max_length=20)
    displaypicture  = models.ImageField(max_length=144, upload_to='uploads/%Y/%m/%d/')

class RoommateInHouse(models.Model):
    roommate    = models.ForeignKey(
                            'Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )
    house       = models.ForeignKey(
                            'House', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )

class House(models.Model):
    name            = models.CharField(max_length=20)
    year            = models.DateField()
    leaseStartDate  = models.DateTimeField()
    leaseEndDate    = models.DateTimeField()


# class Payment(models.Model):
    # owner       = models.ForeignKey()
    # payingto    = models.ForeignKey()

# class Charge(models.Model):
    # owner       = models.ForeignKey()
    # requestfrom = models.ForeignKey()

from django.db import models

# Create your models here.
class Lease(models.Model):
    name        = models.CharField(max_length=15)
    address     = models.CharField(max_length=50)
    startDate   = models.DateField()
    endDate     = models.DateField()

    def __str__(self):
        print("#"+str(self.id), "-", str(self.name))

class Roommate(models.Model):
    name    = models.CharField(max_length=25)
    house   = models.ForeignKey(
                        'Lease', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False
                        )
    # user    = models.ForeignKey()

    def __str__(self):
        print("#"+str(self.id), "-", str(self.name))

class UtilityType(models.Model):
    category    = models.CharField(max_length=8)
    name        = models.TextField(max_length=20)
    website     = models.TextField(max_length=200)
    ServiceType = models.TextField(max_length=50)
    image       = models.ImageField(max_length=200)

    def __str__(self):
        print("#"+str(self.id), "-", str(self.name))

class UtilityBill(models.Model):
    amount          = models.DecimalField(max_digits=6, decimal_places=2)
    dueDate         = models.DateField()
    statementDate   = models.DateField()
    datepaid        = models.DateField()
    house           = models.ForeignKey(
                                'Lease', null=False,
                                blank=False, default="",
                                on_delete=models.SET_DEFAULT,
                                db_constraint=False
                                )
    utilType        = models.ForeignKey(
                                'UtilityType', null=False,
                                blank=False, default="",
                                on_delete=models.SET_DEFAULT,
                                db_constraint=False
                                )

    def __str__(self):
        print("#"+str(self.id), "-", str(self.utilType.name) + "  due: " + str(self.amount) + "  by: " + str(self.dueDate))

class billPayment(models.Model):
    date        = models.DateField()
    amount      = models.DecimalField(max_digits=6, decimal_places=2)
    payType     = models.TextField()
    payer       = models.ForeignKey(
                            'Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )
    UtilBill    = models.ForeignKey(
                            'UtilityBill', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )

class userPayment(models.Model):
    date    = models.DateField()
    amount  = models.DecimalField(max_digits=6, decimal_places=2)
    payType = models.TextField()
    payer   = models.ForeignKey(
                        'Roommate', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False, related_name="payer"
                        )
    payee   = models.ForeignKey(
                        'Roommate', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False, related_name="payee"
                        )

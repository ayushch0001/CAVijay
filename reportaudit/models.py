import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class Cluster (models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.name)

class Customer(models.Model):
    nameOfOrganization = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200,null=False,default="address")
    cluster = models.ForeignKey(Cluster, on_delete=models.PROTECT,default=None)
    block = models.CharField(max_length=200,blank=False, null=False,default="default")
    district = models.CharField(max_length=200,blank=False, null=False,default="default")
    def __str__(self):
        return str(self.nameOfOrganization)
    

class AuditType(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.name)
        
    


class Collection(models.Model):
    id = models.AutoField(primary_key=True,unique=True,auto_created=True)
    
class Month(models.Model):
    id = models.AutoField(primary_key=True,unique=True,auto_created=True)
    month = models.CharField(max_length=8)
    collectionId =  models.ForeignKey(Collection, on_delete=models.PROTECT,default=None)
    
    def __str__(self):
            return str(self.collectionId)
    
class BackendReport(models.Model):
    CASH_OR_BANK_CHOICES = [
        (1, 'Cash'),
        (2, 'Bank'),
    ]

    RECEIPT_OR_PAYMENT_CHOICES = [
        (1, 'Receipt'),
        (2, 'Payment'),
    ]

    auditType = models.ForeignKey(AuditType, on_delete=models.PROTECT, null=True, blank=True)
    title = models.TextField(max_length=255)
    cashOrBank = models.IntegerField(choices=CASH_OR_BANK_CHOICES, default=0,null=False)
    receiptOrPayment = models.IntegerField(choices=RECEIPT_OR_PAYMENT_CHOICES, default=0,null=False)
    dict = models.JSONField(default=dict)  # Renamed `dict` to `report_data`
    month = models.ForeignKey(Month, on_delete=models.PROTECT, null=True, blank=True)
    formula = models.CharField(max_length=4,null=True)


    
    def __str__(self):
            return str(self.title)
            

    

class Audit(models.Model):
    id = models.AutoField(primary_key=True,unique=True,auto_created=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    yearStart = models.IntegerField(default=0)
    yearEnd = models.IntegerField(default=0)
    Udin = models.CharField(max_length=20,blank=False, null=False,default="default")
    Mno = models.CharField(max_length=5,blank=False, null=False,default="444225")
    date = models.DateField(null=True)
    observations = models.TextField(default="")
    observations2 = models.TextField(default="give a true and fair view:")
    def __str__(self):
        return f"{self.customer.nameOfOrganization} - {self.yearStart} - {self.yearEnd} "
    
    

class MainReport(models.Model):
    audit = models.ForeignKey(Audit,on_delete=models.CASCADE)
    def __str__(self) -> str:
         return f"{self.audit.customer} - {self.audit.yearStart} -{self.audit.yearEnd} "
    
    
    
    
class yearReportData(models.Model):   
    yearReports = models.ForeignKey(MainReport, on_delete=models.CASCADE)
    A0 = models.IntegerField(default = 0,null=False)
    B0 = models.IntegerField(default = 0,null=False)
    A1 = models.IntegerField(default = 0,null=False)
    A2 = models.IntegerField(default = 0,null=False)
    A3 = models.IntegerField(default = 0,null=False)
    A4 = models.IntegerField(default = 0,null=False)
    A5 = models.IntegerField(default = 0,null=False)
    A6 = models.IntegerField(default = 0,null=False)
    A7 = models.IntegerField(default = 0,null=False)
    A8 = models.IntegerField(default = 0,null=False)
    A9 = models.IntegerField(default = 0,null=False)
    A10 = models.IntegerField(default = 0,null=False)
    A11 = models.IntegerField(default = 0,null=False)
    A12 = models.IntegerField(default = 0,null=False)
    A13 = models.IntegerField(default = 0,null=False)
    A14 = models.IntegerField(default = 0,null=False)
    A15 = models.IntegerField(default = 0,null=False)
    A16 = models.IntegerField(default = 0,null=False)
    A17 = models.IntegerField(default = 0,null=False)
    A18 = models.IntegerField(default = 0,null=False)
    A19 = models.IntegerField(default = 0,null=False)
    A20 = models.IntegerField(default = 0,null=False)
    A21 = models.IntegerField(default = 0,null=False)
    A22 = models.IntegerField(default = 0,null=False)
    A23 = models.IntegerField(default = 0,null=False)
    A24 = models.IntegerField(default = 0,null=False)
    A25 = models.IntegerField(default = 0,null=False)
    A26 = models.IntegerField(default = 0,null=False)
    A27 = models.IntegerField(default = 0,null=False)
    A28 = models.IntegerField(default = 0,null=False)
    A29 = models.IntegerField(default = 0,null=False)
    A30 = models.IntegerField(default = 0,null=False)
    A31 = models.IntegerField(default = 0,null=False)
    A32 = models.IntegerField(default = 0,null=False)
    A33 = models.IntegerField(default = 0,null=False)
    A34 = models.IntegerField(default = 0,null=False)
    A35 = models.IntegerField(default = 0,null=False)
    A36 = models.IntegerField(default = 0,null=False)
    A37 = models.IntegerField(default = 0,null=False)
    A38 = models.IntegerField(default = 0,null=False)
    A39 = models.IntegerField(default = 0,null=False)
    A40 = models.IntegerField(default = 0,null=False)
    A41 = models.IntegerField(default = 0,null=False)
    A42 = models.IntegerField(default = 0,null=False)
    A43 = models.IntegerField(default = 0,null=False)
    A44 = models.IntegerField(default = 0,null=False)
    A45 = models.IntegerField(default = 0,null=False)
    A46 = models.IntegerField(default = 0,null=False)
    A47 = models.IntegerField(default = 0,null=False)
    A48 = models.IntegerField(default = 0,null=False)
    A49 = models.IntegerField(default = 0,null=False)
    A50 = models.IntegerField(default = 0,null=False)
    A51 = models.IntegerField(default = 0,null=False)
    A52 = models.IntegerField(default = 0,null=False)
    A53 = models.IntegerField(default = 0,null=False)
    A54 = models.IntegerField(default = 0,null=False)
    A55 = models.IntegerField(default = 0,null=False)
    A56 = models.IntegerField(default = 0,null=False)
    A57 = models.IntegerField(default = 0,null=False)
    A58 = models.IntegerField(default = 0,null=False)
    A59 = models.IntegerField(default = 0,null=False)
    A60 = models.IntegerField(default = 0,null=False)
    A61 = models.IntegerField(default = 0,null=False)
    A62 = models.IntegerField(default = 0,null=False)
    A63 = models.IntegerField(default = 0,null=False)
    A64 = models.IntegerField(default = 0,null=False)
    A65 = models.IntegerField(default = 0,null=False)
    A66 = models.IntegerField(default = 0,null=False)
    A67 = models.IntegerField(default = 0,null=False)
    A68 = models.IntegerField(default = 0,null=False)
    A69 = models.IntegerField(default = 0,null=False)
    A70 = models.IntegerField(default = 0,null=False)
    
    B1 = models.IntegerField(default = 0,null=False)
    B2 = models.IntegerField(default = 0,null=False)
    B3 = models.IntegerField(default = 0,null=False)
    B4 = models.IntegerField(default = 0,null=False)
    B5 = models.IntegerField(default = 0,null=False)
    B6 = models.IntegerField(default = 0,null=False)
    B7 = models.IntegerField(default = 0,null=False)
    B8 = models.IntegerField(default = 0,null=False)
    B9 = models.IntegerField(default = 0,null=False)
    B10 = models.IntegerField(default = 0,null=False)
    B11 = models.IntegerField(default = 0,null=False)
    B12 = models.IntegerField(default = 0,null=False)
    B13 = models.IntegerField(default = 0,null=False)
    B14 = models.IntegerField(default = 0,null=False)
    B15 = models.IntegerField(default = 0,null=False)
    B16 = models.IntegerField(default = 0,null=False)
    B17 = models.IntegerField(default = 0,null=False)
    B18 = models.IntegerField(default = 0,null=False)
    B19 = models.IntegerField(default = 0,null=False)
    B20 = models.IntegerField(default = 0,null=False)
    B21 = models.IntegerField(default = 0,null=False)
    B22 = models.IntegerField(default = 0,null=False)
    B23 = models.IntegerField(default = 0,null=False)
    B24 = models.IntegerField(default = 0,null=False)
    B25 = models.IntegerField(default = 0,null=False)
    B26 = models.IntegerField(default = 0,null=False)
    B27 = models.IntegerField(default = 0,null=False)
    B28 = models.IntegerField(default = 0,null=False)
    B29 = models.IntegerField(default = 0,null=False)
    B30 = models.IntegerField(default = 0,null=False)
    B31 = models.IntegerField(default = 0,null=False)
    B32 = models.IntegerField(default = 0,null=False)
    B33 = models.IntegerField(default = 0,null=False)
    B34 = models.IntegerField(default = 0,null=False)
    B35 = models.IntegerField(default = 0,null=False)
    B36 = models.IntegerField(default = 0,null=False)
    B37 = models.IntegerField(default = 0,null=False)
    B38 = models.IntegerField(default = 0,null=False)
    B39 = models.IntegerField(default = 0,null=False)
    B40 = models.IntegerField(default = 0,null=False)
    B41 = models.IntegerField(default = 0,null=False)
    B42 = models.IntegerField(default = 0,null=False)
    B43 = models.IntegerField(default = 0,null=False)
    B44 = models.IntegerField(default = 0,null=False)
    B45 = models.IntegerField(default = 0,null=False)
    B46 = models.IntegerField(default = 0,null=False)
    B47 = models.IntegerField(default = 0,null=False)
    B48 = models.IntegerField(default = 0,null=False)
    B49 = models.IntegerField(default = 0,null=False)
    B50 = models.IntegerField(default = 0,null=False)
    B51 = models.IntegerField(default = 0,null=False)
    B52 = models.IntegerField(default = 0,null=False)
    B53 = models.IntegerField(default = 0,null=False)
    B54 = models.IntegerField(default = 0,null=False)
    B55 = models.IntegerField(default = 0,null=False)
    B56 = models.IntegerField(default = 0,null=False)
    B57 = models.IntegerField(default = 0,null=False)
    B58 = models.IntegerField(default = 0,null=False)
    B59 = models.IntegerField(default = 0,null=False)
    B60 = models.IntegerField(default = 0,null=False)
    B61 = models.IntegerField(default = 0,null=False)
    B62 = models.IntegerField(default = 0,null=False)
    B63 = models.IntegerField(default = 0,null=False)
    B64 = models.IntegerField(default = 0,null=False)
    B65 = models.IntegerField(default = 0,null=False)
    B66 = models.IntegerField(default = 0,null=False)
    B67 = models.IntegerField(default = 0,null=False)
    B68 = models.IntegerField(default = 0,null=False)
    B69 = models.IntegerField(default = 0,null=False)
    B70 = models.IntegerField(default = 0,null=False)



    # this are for the text contents to save s
    EA1 = models.TextField(default="")
    EA2 = models.TextField(default="")
    EA3 = models.TextField(default="")
    EA4 = models.TextField(default="")
    EA5 = models.TextField(default="")
    EA6 = models.TextField(default="")
    EA7 = models.TextField(default="")
    EA8 = models.TextField(default="")
    EA9 = models.TextField(default="")
    EA10 = models.TextField(default="")
    EA11 = models.TextField(default="")
    EA12 = models.TextField(default="")
    EA13 = models.TextField(default="")
    EA14 = models.TextField(default="")
    EA15 = models.TextField(default="")
    EA16 = models.TextField(default="")
    EA17 = models.TextField(default="")
    
    EB1 = models.TextField(default="")
    EB2 = models.TextField(default="")
    EB3 = models.TextField(default="")
    EB4 = models.TextField(default="")
    EB5 = models.TextField(default="")
    EB6 = models.TextField(default="")
    EB7 = models.TextField(default="")
    EB8 = models.TextField(default="")
    EB9 = models.TextField(default="")
    EB10 = models.TextField(default="")
    EB11 = models.TextField(default="")
    EB12 = models.TextField(default="")
    EB13 = models.TextField(default="")
    EB14 = models.TextField(default="")
    EB15 = models.TextField(default="")
    EB16 = models.TextField(default="")
    EB17 = models.TextField(default="")
    EB18 = models.TextField(default="")  
    EB19 = models.TextField(default="")
    EB20 = models.TextField(default="")

    def __str__(self) -> str:
         return f"{self.yearReports.audit.customer} - {self.yearReports.audit.yearStart} -{self.yearReports.audit.yearEnd} "
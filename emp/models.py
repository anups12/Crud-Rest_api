from django.db import models

# Create your models here.
choices=[('pending','pending'),('completed','completed')]

class Employee(models.Model):
    name= models.CharField(max_length=250)
    dob = models.DateField()
    email = models.EmailField(max_length=150, unique=True)
    phone = models.PositiveIntegerField()
    status = models.CharField(choices=choices, max_length=10)

    def __str__(self):
        return self.name



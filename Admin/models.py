from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)

class JobSeeker(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=300, null=True)
    expected_salary = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    experience = models.CharField(max_length=128, null=True, blank=True)
    available = models.BooleanField(default=True, null=True, blank=False)
    id_proof = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        return url

class CustomerDetials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    mobile_number = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    place = models.CharField(max_length=128, null=True, blank=True)
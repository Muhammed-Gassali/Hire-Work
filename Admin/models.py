from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    
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


class Collection(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)

    @property
    def get_total(self):
        total = self.seeker.expected_salary 
        return total

class order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=128, null=True, blank=True)
    place = models.CharField(max_length=128, null=True, blank=True)
    land_mark = models.CharField(max_length=128, null=True, blank=True)
    pincode = models.CharField(max_length=128, null=True, blank=True)
    time =models.TimeField()
    date = models.DateField()
    order_verify = models.BooleanField(default=False, null=True, blank=False)
    customer_cancel = models.BooleanField(default=True, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)


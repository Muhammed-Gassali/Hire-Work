from rest_framework import serializers
from Admin.models import *

class SerializeCustomerHomepage(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SerilazeSeekerCarpenterDetials(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = "__all__"

class SerializeCustomer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

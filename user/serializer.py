from rest_framework import serializers
from Admin.models import *

class SerializeCustomerHomepage(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = "__all__"
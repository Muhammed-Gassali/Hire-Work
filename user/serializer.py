from rest_framework import serializers
from Admin.models import *

class SerializeCustomerHomepage(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
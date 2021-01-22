from rest_framework import serializers
from userpost.models import PassportDataModel

class PassportPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PassportDataModel
        fields = '__all__'

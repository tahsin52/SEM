from rest_framework import serializers

from core.models import CarModel


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = '__all__'



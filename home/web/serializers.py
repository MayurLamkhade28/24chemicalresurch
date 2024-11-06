from rest_framework import serializers
from .models import Title, Datatable, Category, Report_price, Cart


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'  # This will include all fields in the model


class DatatableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datatable
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class meta:
        model = Category
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class meta:
        model = Report_price
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class meta:
        model = Cart
        fields = '__all__'

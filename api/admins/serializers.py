from rest_framework.response import Response
from rest_framework import serializers, exceptions
from rest_framework.fields import CurrentUserDefault
from main.models import *
from api.serializers import *

class AdminCategorySerialzier(serializers.ModelSerializer):
  class Meta:
    fields = '__all__'
    model = Category

class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class AdminResturantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resturant
        fields = '__all__'

class AdminOrderItemSerializer(serializers.ModelSerializer):
    product = AdminProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total']

class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField(method_name='get_status_display')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'status', 'status_display', 'user']

    def get_status_display(self, inst):
        return inst.get_status_display()
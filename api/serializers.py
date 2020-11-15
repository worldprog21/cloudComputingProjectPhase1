from rest_framework.response import Response
from rest_framework import serializers, exceptions
from rest_framework.fields import CurrentUserDefault
from main.models import *


class MediaSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    medium = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            self.request = None
        super(MediaSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def build_url(self, url):
        if self.request:
            return self.request.build_absolute_uri(url)
        elif 'request' in self.context:
            return self.context['request'].build_absolute_uri(url)
        elif 'view' in self.context:
            return self.context['view'].request.build_absolute_uri(url)
        return url

    def get_thumbnail(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.thumbnail.url)

    def get_medium(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.medium.url)

    def get_large(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.large.url)

    def get_file(self, obj):
        return self.build_url(self, obj.file.url)

    class Meta:
        model = Media
        fields = ['id', 'name', 'file', 'thumbnail', 'medium', 'large']

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name', 'email']

class ResturantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resturant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    resturant = ResturantSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField(method_name='get_status_display')
    resturant = ResturantSerializer(read_only=True)
    resturant_id = serializers.PrimaryKeyRelatedField(queryset=Resturant.objects.filter(is_open=True), required=True, source='resturant')

    class Meta:
        model = Order
        fields = ['id','resturant_id', 'resturant', 'items', 'status_display']

    def get_status_display(self, inst):
        return inst.get_status_display()
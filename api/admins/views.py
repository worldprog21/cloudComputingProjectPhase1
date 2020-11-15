from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.viewsets import *
from api.serializers import *
from api.admins.serializers import *
from main.models import *
from api.admins.serializers import *
from api.utils import *

class AdminMediaViewSet(ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()

class AdminProductViewSet(ModelViewSet):
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all()
    filterset_fields = ['category__id']

    def get_queryset(self):
        return super().get_queryset().filter(resturant=self.request.user.admin.resturant)


class AdminCategoryViewSet(ModelViewSet):
    serializer_class = AdminCategorySerialzier
    queryset = Category.objects.all()

class AdminResturantViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = AdminResturantSerializer
    queryset = Resturant.objects.all()

    def get_object(self):
        return self.request.user.admin.resturant

class AdminOrderViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = AdminOrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(resturant=self.request.user.admin.resturant).exclude(status=0)
    
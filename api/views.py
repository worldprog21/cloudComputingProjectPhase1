from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from api.serializers import *
from main.models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login

# Create your views here.
class TestView(APIView):
    def get(self, *args, **kwargs):
        return Response({"working"})

class UsernamePasswordAuth(ObtainAuthToken):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })

class MediaViewSet(ReadOnlyModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()

class ResturantViewSet(ReadOnlyModelViewSet):
    serializer_class = ResturantSerializer
    queryset = Resturant.objects.filter(is_open=True)

class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filterset_fields = ['resturant__id']

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_current_object(self):
        return self.get_queryset().filter(status=0).first() or None

    def perform_create(self, serializer):
        obj = self.get_current_object()
        if obj:
            raise Exception('You have pending order to complete. please delete order with id : ' + str(obj.id))

        serializer.save(user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.status != 0:
            raise Exception('You just can delete "created" orders.')
        instance.delete()

    def add_item(self, request, *args, **kwargs):
        product_id = int(kwargs['product_id'])
        order = self.get_current_object()
        try:
            product = Product.objects.get(pk=product_id)
            if not product.resturant.is_open:
                raise Exception('Resturant is closed.')
            if product.resturant != order.resturant:
                raise Exception('You should complete or delete current order first.')
            order_item, _c = OrderItem.objects.get_or_create(order=order, product=product)
            if not _c:
                order_item.quantity += 1
                order_item.save()
            return Response(self.serializer_class(order).data)
        except Product.DoesNotExist:
            raise Exception('Product not found.')

    def remove_item(self, request, *args, **kwargs):
        product_id = int(kwargs['product_id'])
        order = self.get_current_object()
        try:
            order_item = OrderItem.objects.get(product__id=product_id, order=order)
            if order_item.quantity == 1:
                order_item.delete()
            else:
                order_item.quantity -= 1
                order_item.save()
            return Response(self.serializer_class(order).data)
        except OrderItem.DoesNotExist:
            raise Exception('Product not found.')

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        order = self.get_current_object()
        if not order:
            raise Exception('Order not found')
        order.status = 1
        order.save()
        return Response(self.serializer_class(order).data)
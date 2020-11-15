from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from api.views import *
from api.admins.views import *

#User
router = routers.SimpleRouter()
router.register(r'medias', MediaViewSet)
router.register(r'resturants', ResturantViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'admin/medias', AdminMediaViewSet)
router.register(r'admin/products', AdminProductViewSet)
router.register(r'admin/categories', AdminCategoryViewSet)
router.register(r'admin/orders', AdminOrderViewSet)

urlpatterns = router.urls

#User
urlpatterns += [
    path('auth/login/', UsernamePasswordAuth.as_view()),
    path('orders/<int:pk>/add_item/<product_id>/', OrderViewSet.as_view({'post': 'add_item'})),
    path('orders/<int:pk>/remove_item/<product_id>/', OrderViewSet.as_view({'post': 'remove_item'})),
    path('admin/resturant/', AdminResturantViewSet.as_view({'get' : 'retrieve', 'put' : 'update', 'delete': 'destroy'}))
    # router.register(r'admin/resturants', AdminResturantViewSet)
]

#Admin
urlpatterns += [
    # path('admin/users/<int:pk>/update_password/', AdminChangeUserPasswordView.as_view() ),
]
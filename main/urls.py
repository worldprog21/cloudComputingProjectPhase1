from django.urls import path, include
from main.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('p/<int:code>/', ProductDetailView.as_view(), name='product-detail'),
]
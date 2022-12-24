from django.urls import path

from core.api.views import *

urlpatterns = [
    path('get_data/', get_car_data, name='get_car_data'),
    path('data/', CarViewSet.as_view({'get': 'list', 'post': 'create'}), name='car_list'),
]
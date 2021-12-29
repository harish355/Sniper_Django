from django.urls import path

from . import views

urlpatterns = [
    path('', views.OpenOrderList.as_view(), name='OpenOrder'),
    path('cancel/',views.Cancel_open_order.as_view(),name="Cancel Open Order"),
    path('squareoff/',views.Square_Off.as_view(),name="Square Off"),
    path('close/', views.Close_Open_Order.as_view(), name='Close_Open_order')
]

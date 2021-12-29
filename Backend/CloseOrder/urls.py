from django.urls import path

from . import views

urlpatterns = [
    path('', views.CloseOrder.as_view(), name='OpenOrder'),
    path('delete/', views.Delete_Close_Order.as_view(),
         name="Delete_Cancel_order"),
    path('clear_all/', views.Clear_All_CloseOrder.as_view(), name="Clear_All"),
]

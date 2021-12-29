from django.urls import path

from . import views

urlpatterns = [
    path('', views.CancelOrderList.as_view(), name='OpenOrder'),
    path('delete/', views.Delete_CancelOrder.as_view(),
         name="Delete_Cancel_order"),
    path('clear_all/', views.Clear_All_CancelOrder.as_view(), name="Clear_All"),
]

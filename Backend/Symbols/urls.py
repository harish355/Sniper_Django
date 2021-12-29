from django.urls import path
from django.views.generic.base import View

from . import views

urlpatterns = [
    path('', views.Symbols_watch_list.as_view(), name='Get List of Symbols'),
    path('update/', views.Update_Symbols.as_view(), name='Update Symbols'),
    path('delete/', views.Delete_Symbols.as_view(), name='Delete'),
    path('list',views.List_of_Symbols.as_view(),name="List_of_Symbols"),
    path('buy/', views.Buy_Symbols.as_view(), name="Buy Symbols"),

    path('order',views.Buy_Sell.as_view(),name="Place order")
]

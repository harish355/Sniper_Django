from django.urls import path

from . import views

urlpatterns = [
    path('', views.Desktop_Trade.as_view(), name='Trade'),
    path('login',views.Login.as_view(),name='Login'),

]

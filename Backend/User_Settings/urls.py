from django.urls import path

from . import views

urlpatterns = [
    path('', views.API_Data.as_view(), name='Submit User Data'),
    path('update/',views.API_update.as_view(),name='Update api Data'),
    path('session_id/',views.User_Api_SessionId.as_view(),name="Session Id")

]

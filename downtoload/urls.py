from django.urls import path
from . import views


urlpatterns = [
    path('', views.download_view, name='download_video'),
    path('home/', views.home, name='home'),
    path("hello/", views.hello, name='hello'),
       path("message/", views.message, name='message'),
       path("action/", views.action_handler, name='action-handler'),
    # path('download/', views.download_view, name='download_video'),
]

from django.urls import path


from . import views


urlpatterns = [
    path('header/', views.test_header, name='header'),
]
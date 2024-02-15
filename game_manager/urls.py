from django.urls import path


from . import views


urlpatterns = [
    path('create/', views.create_session, name='create_session'),
    path('new_game/', views.start_new_game, name='create_new_game'),
    path('info/', views.get_session_info, name='get_session_info'),
    path('place_bet/<int:bet_amount>/', views.place_bet),
    path('hit/', view=views.hit),
    path('stand/', view=views.stand, name='stand')
]
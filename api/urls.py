from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('user/', views.user_info),
    path('review/', views.missed_data),
    path('random/', views.random_data),
    path('all/', views.all_data),
    path('result/', views.result),
]

from django.urls import path
from . import views

app_name = 'systan'
urlpatterns = [
    path('login/', views.login_prompt, name="login_prompt"),
    path('words/', views.words, name='words'),
    path('words/<student_id>/', views.words_individual, name='words_individual'),
    path('phrases/', views.phrases, name='phrases'),
    path('phrases/<student_id>/', views.phrases_individual, name='phrases_individual'),
    path('tests/<type>/<stage>/<mode>/', views.tests, name='tests'),
    path('tests/<type>/<stage>/<mode>/<student_id>/', views.tests_individual, name='tests_individual'),
    path('show/<type>/<stage>/<mode>/', views.show, name='show'),
    path('show/<type>/<stage>/<mode>/<student_id>/', views.show_individual, name='show_individual'),
    path('game_data_post/', views.game_data_post, name='game_data_post'),
    path('others/', views.others, name='others')
]
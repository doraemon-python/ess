from django.urls import path
from . import views

app_name = 'systan'
urlpatterns = [
    path('login/', views.login_prompt, name="login_prompt"),
    path('<type>/<student_id>/', views.home, name='home'),
    path('chapter_select/<type>/<category>/<stage>/<mode>/<student_id>/', views.chapter_select, name='chapter_select'),
    path('<type>/<category>/<stage>/<chapter>/<mode>/<student_id>/', views.tests, name='tests'),
    path('others/<type>/<student_id>', views.others, name='others'),
    path('game_data_post/', views.game_data_post, name='game_data_post'),
]

# type: words, phrases
# category: tests, show
# stage: Stage1, 2, 3, 4, 5
# chapter: int 1 ~ 3, 4, 5, 6 all
# mode: review, random, all
# student_id: int 1 ~ 999
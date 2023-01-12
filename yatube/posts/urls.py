from django.contrib import admin
from django.urls import path


from . import views


urlpatterns = [
# правила для сопоставления шаблонов URL и функций
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('new/', views.new_post, name='new_post'),
    # Профайл пользователя
    path('follow/', views.follow_index, name='follow_index'),
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр поста
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    # Редактирование поста
    path('<str:username>/<int:post_id>/edit/',
        views.post_edit, name='post_edit'),
    # Подписка 
    path('<str:username>/follow/', views.profile_follow,
         name='profile_follow'),
    # Отписка
    path('<str:username>/unfollow/', views.profile_unfollow,
         name='profile_unfollow'),
    # path('<username>/<int:post_id>/comment/', views.add_comment, name='add_comment')
    path('', views.index, name='index')
]

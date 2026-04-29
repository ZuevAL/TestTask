from django.urls import path
from . import views


app_name = 'application'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),
    path('manage_rules/', views.manage_rules, name='manage_rules'),
]
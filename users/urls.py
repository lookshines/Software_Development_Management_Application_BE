from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('create-project/', views.create_project, name='create_project'),
    path('profile/update/', views.update_profile, name='updatep_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('user/delect/<user_id>/', views.delete_user, name='delete_user'),
    path('user/deactivate/<user_id>/', views.deactivate_user, name='deactivate_user'),
    path('user/reactivate/<user_id>/', views.reactivate_user, name='reactivate_user'),
    path('user/get-users/', views.get_users, name='get_users'),
    path('user/get-user/<int:id>/', views.get_user, name='get_user'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

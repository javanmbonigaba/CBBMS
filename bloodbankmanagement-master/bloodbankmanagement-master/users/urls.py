from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
    path('user_login', views.user_login,name='user_login'),
    path('user_dashboard_view', views.user_dashboard_view,name='user_dashboard_view'),
    path('logout', LogoutView.as_view(template_name='blood/logout.html'),name='logout'),

    
]
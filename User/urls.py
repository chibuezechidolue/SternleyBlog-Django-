from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('register/', views.register_page,name="register-page"),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'),name="login"),
    
]
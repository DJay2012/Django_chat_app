from django.urls import path
from. import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('chat/<int:user_id>/', views.chat, name='chat_with_user'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='chat'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
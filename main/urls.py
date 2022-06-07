from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',views.loginUser, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerUser, name="register"),
    path('', views.home,name="home"),
    path('home/', views.home,name="home"),
    path('aboutus/', views.aboutus,name="aboutus"),
    path('terms/', views.terms,name="terms"),
    path('contactus/', views.contactus,name="contactus"),
    path('tools/', views.tools,name="tools"),  

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="main/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="main/password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/update_password.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="main/reset_password_complete.html"), name="password_reset_complete"), 
]

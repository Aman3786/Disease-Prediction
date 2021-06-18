from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('registration/' , views.register_uer,name="register"),
    path("login/", views.login_request, name="login"),
    path("home/", views.home, name="home"),
    path("doctor_info/", views.Doctor_info,name="doctor_info"),
    path('logout/',views.Logout,name="logout"),
    path("profile/",views.doctor_profile,name="profile"),
    path('doctor_page/',views.doctor_page,name="doctor_page"),
    path('testing',views.just_for_testing,name="just_for_testing"),
    path('reset_password/',auth_view.PasswordResetView.as_view(template_name="password/password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(template_name="password/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name="password/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password/password_reset_done.html'),name="password_reset_complete"),

]
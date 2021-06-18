"""prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('', views.home_page,name="home_page"),
    # path('test/', views.test_page, name='test'),
    path('pneumonia/', views.pneumonia, name='pneumonia'),
    path('covid/', views.covid, name='covid'),
    path('predict_covid/', views.predict_covid, name='predict_covid'),
    path('predict_pneumonia/', views.predict_pneumonia, name='predict_pneumonia'),
    path('brain/', views.brain, name='brain'),
    path('predict_brain_tumor/', views.predict_brain_tumor, name='predict_brain_tumor'),
    path('breast_cancer/', views.breast_cancer, name='breast_cancer'),
    path('predict_breast_cancer/', views.predict_breast_cancer, name='predict_breast_cancer'),
    path('heart/', views.heart, name='heart'),
    path('predict_heart_disease/', views.predict_heart_disease, name='predict_heart_disease'),
    # path('send_mail/' ,views.sendEmail),
    # path('email/',include(mail_urls)),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


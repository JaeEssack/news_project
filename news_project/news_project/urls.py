from django.contrib import admin
from django.urls import path, include
from news_app import views

urlpatterns = [
    path('', views.redirect_dashboard, name='redirect_dashboard'),  # optional
    path('', include('news_app.urls')),
    path('admin/', admin.site.urls),
]
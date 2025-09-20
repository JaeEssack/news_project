"""
URL configuration for the news_app Django application.

Maps URL patterns to their corresponding views for readers, journalists, editors, 
and authentication.
"""


from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from news_app.views import CustomLogoutView

urlpatterns = [
    # Redirect to role-specific dashboard   
    path('', views.redirect_dashboard, name='redirect_dashboard'),

    # Reader URLs
    path('reader/', views.reader_dashboard, name='reader_dashboard'),
    path('reader/subscribe/<int:publisher_id>/', views.subscribe_publisher, name='subscribe_publisher'),
    path('reader/unsubscribe/<int:publisher_id>/', views.unsubscribe_publisher, name='unsubscribe_publisher'),
    path('reader/follow/<int:journalist_id>/', views.follow_journalist, name='follow_journalist'),
    path('reader/unfollow/<int:journalist_id>/', views.unfollow_journalist, name='unfollow_journalist'),

    # Journalist URLs
    path('journalist/', views.journalist_dashboard, name='journalist_dashboard'),
    path('journalist/create/', views.create_article, name='create_article'),

    # Editor URLs
    path('editor/', views.editor_dashboard, name='editor_dashboard'),
    path('editor/approve/<int:article_id>/', views.approve_article, name='approve_article'),

    # Auth URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
]



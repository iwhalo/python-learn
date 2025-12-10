from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('rsvp/', views.rsvp_form, name='rsvp'),
    path('submit-rsvp/', views.submit_rsvp, name='submit_rsvp'),
    path('countdown/', views.countdown, name='countdown'),
    path('gallery/', views.gallery, name='gallery'),
    path('map/', views.map_location, name='map'),
    path('guests/', views.guest_list, name='guest_list'),
    path('api/guest-stats/', views.guest_stats_api, name='guest_stats_api'),
]
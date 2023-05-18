from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('toggle-online-status/', toggle_online_status, name='toggle-online-status'),
    path('connection/', connection, name='connection'),
    path('connect-establish/',connect_establish, name='connect-establish'),
    path('connected/', connected, name='connected'),
    path('logout/', logout_view, name='logout'),
  
]

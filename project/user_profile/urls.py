from django.urls import path, include

from user_profile.views import user_profile

app_name = 'user_profile'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('<name>',user_profile, name='user_profile'),
]
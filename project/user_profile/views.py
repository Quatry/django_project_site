from django.shortcuts import render, redirect

from app.models import User


def user_profile(request,name):
    user_info = User.objects.filter(username = name).get()
    owner = request.user.id
    return render(request,
                  'user_profile.html',
                  {'user_info':user_info,
                   'owner':owner,
                   })

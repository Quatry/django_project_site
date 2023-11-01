from django.shortcuts import render, redirect

from app.models import User, Project, Participant


def user_profile(request,name):
    user_info = User.objects.filter(username = name).get()
    user_projects = Project.objects.filter(owner = user_info.id).all()
    user_participant = Participant.objects.filter(participant = user_info.id).all()
    owner = request.user.id
    return render(request,
                  'user_profile.html',
                  {'user_info':user_info,
                   'owner':owner,
                   'user_projects':user_projects,
                   'user_participant':user_participant
                   })

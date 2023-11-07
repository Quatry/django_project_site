from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import UserCreationForm, ProjectCreationForm, ParticipantAddForm, ProjectEditForm, ProjectUpdateAddForm, \
    ProjectEventAddForm
from app.models import Project, Participant, ProjectUpdate, ProjectEvent
from app.service import _create_project, _home_page, Project_page, _edit_project_post, _invite_page_info, \
    _add_participant_post, _add_update_post, _add_event_post


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def create_project(request):
    if request.method == "POST":
        _create_project(request)
        return redirect('home')
    project = ProjectCreationForm()
    return render(request,
                  'create_project.html',
                  {'project': project}
                  )


def home_page(request):
    info = _home_page(request)
    return render(request,
                  'home.html',
                  info,
                  )


def project(request, project_id):
    if request.method == 'POST':
        dir = Project_page()._project_post(request, project_id)
        return redirect(dir)
    info = Project_page()._project_info(request, project_id)
    return render(request, 'project.html', info)


def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.id == project.owner.id:
        if request.method == 'POST':
            _edit_project_post(request, project)
            return redirect('home')
        elif request.method == 'GET':
            return render(request,
                          'edit_project.html',
                          {'project': project,
                           })
    return redirect('home')


def invite(request):
    info = _invite_page_info(request)
    return render(request, 'invite.html', info)


def add_participant(request, project_id):
    if request.method == 'POST':
        _add_participant_post(request, project_id)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        participant = ParticipantAddForm()
    return render(request,
                  'add_participant.html',
                  {'participant': participant,
                   })


def add_update(request, project_id):
    if request.method == 'POST':
        _add_update_post(request, project_id)
        return redirect(f'../{project_id}')
    else:
        update = ProjectUpdateAddForm()
    return render(request, 'add_update.html', {
        'update': update,
    })


def add_event(request, project_id):
    if request.method == 'POST':
        _add_event_post(request, project_id)
        return redirect(f'../{project_id}')
    else:
        event = ProjectEventAddForm()
    return render(request, 'add_event.html', {
        'event': event,
    })

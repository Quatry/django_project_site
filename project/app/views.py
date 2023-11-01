from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import UserCreationForm, ProjectCreationForm, ParticipantAddForm, ProjectEditForm
from app.models import Project, Participant


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
    if request.method == 'POST':
        project = ProjectCreationForm(request.POST)
        if project.is_valid():
            form = project.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect('home')
    else:
        project = ProjectCreationForm()
    return render(request,
                  'create_project.html',
                  {'project': project}
                  )


def home_page(request):
    projects = "Войдите в систему"
    all_projects = Project.objects.all()
    user = request.user.id
    participant = None
    check_invite = None
    if request.user.is_authenticated:
        participant = Participant.objects.filter(participant=request.user.id).all
        projects = Project.objects.filter(owner=request.user.id)
        check_invite = Participant.objects.filter(participant=request.user.id, invite_status=False).all
    return render(request,
                  'home.html',
                  {'projects': projects,
                   'all_projects': all_projects,
                   'participant': participant,
                   'check_invite': check_invite,
                   'user_id': user,
                   }
                  )


def project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user.id
    participant = Participant.objects.filter(project=project_id).all()
    try:
        participant_invite = Participant.objects.filter(participant=request.user.id, project=project_id).get()
    except Participant.DoesNotExist:
        participant_invite: None = None
    if request.method == 'POST':
        if request.POST.get('join'):
            participant_invite.invite_status = True
            participant_invite.save()
        elif request.POST.get('decline'):
            participant_invite.delete()
        elif request.POST.get('leave'):
            participant_invite.delete()
        elif request.POST.get('delete_project'):
            project.delete()
            return redirect('home')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request,
                  'project.html',
                  {'project': project,
                   'participant_invite': participant_invite,
                   'participant': participant,
                   'user_id': user},
                  )


def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.id == project.owner.id:
        if request.method == 'POST':
            form = ProjectEditForm(request.POST, instance=project)
            if form.is_valid():
                project.save()
                messages.success(request, 'Проект был обновлен!')
                return redirect('home')
        elif request.method == 'GET':
            return render(request,
                          'edit_project.html',
                          {'project': project,
                           }
                          )
    return redirect('home')

def invite(request):
    participant = Participant.objects.filter(participant=request.user.id, invite_status=False).all()
    projects = Project.objects.all()
    return render(request, 'invite.html', {'participant': participant, 'projects': projects})


def add_participant(request, project_id):
    if request.method == 'POST':
        participant = ParticipantAddForm(request.POST)
        this_project = Project.objects.filter(id=project_id).get()
        if participant.is_valid():
            try:
                check_user_is_invited = Participant.objects.filter(project = project_id, participant = request.POST.get('participant')).get()
            except:
                participant = participant.save(commit=False)
                participant.project = this_project
                participant.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        participant = ParticipantAddForm()
    return render(request,
                  'add_participant.html',
                  {'participant': participant,
                   })

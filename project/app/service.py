from django.contrib import messages
from django.shortcuts import get_object_or_404

from app.forms import ProjectCreationForm, ProjectEditForm, ParticipantAddForm, ProjectUpdateAddForm, \
    ProjectEventAddForm
from app.models import Participant, Project, ProjectUpdate, ProjectEvent


def _create_project(request) -> None:
    project = ProjectCreationForm(request.POST)
    if project.is_valid():
        form = project.save(commit=False)
        form.owner = request.user
        form.save()


def _home_page(request) -> dict:
    projects = "Войдите в систему"
    all_projects = Project.objects.all()
    user = request.user.id
    participant = None
    check_invite = None
    if request.user.is_authenticated:
        participant = Participant.objects.filter(participant=request.user.id).all
        projects = Project.objects.filter(owner=request.user.id)
        check_invite = Participant.objects.filter(participant=request.user.id,
                                                  invite_status=False
                                                  ).all
    return {'projects': projects,
            'all_projects': all_projects,
            'participant': participant,
            'check_invite': check_invite,
            'user_id': user,
            }


def _edit_project_post(request, project) -> None:
    form = ProjectEditForm(request.POST, instance=project)
    if form.is_valid():
        project.save()
        messages.success(request, 'Проект был обновлен!')


def _invite_page_info(request) -> dict:
    participant = Participant.objects.filter(participant=request.user.id, invite_status=False).all()
    projects = Project.objects.all()
    return {'projects': projects, 'participant': participant}


def _add_participant_post(request, project_id) -> None:
    participant = ParticipantAddForm(request.POST)
    this_project = Project.objects.filter(id=project_id).get()
    if participant.is_valid():
        if Participant.objects.filter(project=project_id, participant=request.POST.get('participant')).exists():
            pass
        else:
            participant = participant.save(commit=False)
            participant.project = this_project
            participant.save()


def _add_update_post(request, project_id) -> None:
    update = ProjectUpdateAddForm(request.POST)
    this_project = Project.objects.filter(id=project_id).get()
    if update.is_valid():
        update = update.save(commit=False)
        update.project = this_project
        update.save()


def _add_event_post(request, project_id) -> None:
    event = ProjectEventAddForm(request.POST)
    this_project = Project.objects.filter(id=project_id).get()
    if event.is_valid():
        event = event.save(commit=False)
        event.project = this_project
        event.save()


class Project_page():

    def _project_info(self, request, project_id) -> dict:
        project = self._get_project(project_id)
        user = request.user.id
        participant = Participant.objects.filter(project=project_id).all()
        update = ProjectUpdate.objects.filter(project=project_id).all()
        event = ProjectEvent.objects.filter(project=project_id).all()
        participant_invite = self._get_participant(request, project_id)
        return {'project': project,
                'participant_invite': participant_invite,
                'participant': participant,
                'update': update,
                'event': event,
                'user_id': user}

    def _get_project(self, project_id):
        return get_object_or_404(Project, id=project_id)

    def _get_participant(self, request, project_id):
        participant_invite = Participant.objects.filter(
            participant=request.user.id,
            project=project_id
        ).exists()
        if participant_invite:
            participant_invite = Participant.objects.filter(
                participant=request.user.id,
                project=project_id
            ).get()
        else:
            participant_invite = None
        return participant_invite

    def _project_post(self, request, project_id) -> dir:
        project = self._get_project(project_id)
        participant_invite = self._get_participant(request, project_id)
        if request.POST.get('join'):
            participant_invite.invite_status = True
            participant_invite.save()
        elif request.POST.get('decline'):
            participant_invite.delete()
        elif request.POST.get('leave'):
            participant_invite.delete()
        elif request.POST.get('delete_project'):
            project.delete()
            return 'home'
        return request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')

from django.urls import path, include

from app.views import Register, create_project, project, edit_project, invite, add_participant, add_update, add_event

app_name = 'app'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('create_project/', create_project, name='create_project'),
    path('<int:project_id>', project, name = 'project'),
    path('edit/<int:project_id>', edit_project, name='edit_project'),
    path('add_participant/<int:project_id>', add_participant, name='add_participant'),
    path('add_update/<int:project_id>', add_update, name='add_update'),
    path('add_event/<int:project_id>',add_event,name='add_event'),
    path('invites/', invite, name='invite'),
]

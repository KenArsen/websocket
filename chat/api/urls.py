from django.urls import path
from .apis import AddUserToGroupAPI, RemoveUserFromGroupAPI, UserGroupListAPI

urlpatterns = [
    path('groups/', UserGroupListAPI.as_view(), name='user-group-list'),
    path('groups/<int:group_id>/add_user/', AddUserToGroupAPI.as_view(), name='add-user-to-group'),
    path('groups/<int:group_id>/remove_user/', RemoveUserFromGroupAPI.as_view(), name='remove-user-from-group'),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_users, name="properties_owner_index"),
    path("owners/users/create/", views.create_user, name="create_owner_user"),
    path("owners/users/", views.list_users, name="list_owner_users"),
    path("owners/users/<uuid:id>/", views.user_detail, name="owner_user_detail"),
    path("owners/users/<uuid:id>/update/", views.update_user, name="update_owner_user"),
    path("owners/users/<uuid:id>/delete/", views.delete_user, name="delete_owner_user"),
]

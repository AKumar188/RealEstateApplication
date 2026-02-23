from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("admin/users", views.admin_list_users, name="admin_list_users"),
    path("admin/users/<int:id>/block", views.admin_block_user, name="admin_block_user"),
    path("admin/properties", views.admin_list_properties, name="admin_list_properties"),
    path(
        "admin/properties/<int:id>/approve",
        views.admin_approve_property,
        name="admin_approve_property",
    ),
    path(
        "admin/properties/<int:id>/reject",
        views.admin_reject_property,
        name="admin_reject_property",
    ),
]

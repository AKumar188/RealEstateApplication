from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import users, properties
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def _is_admin_request(request):
    if hasattr(request, "user") and getattr(request.user, "is_authenticated", False):
        user_role = getattr(request.user, "role", None)
        if user_role == "admin":
            return True

    admin_user_id = request.headers.get("X-Admin-User-Id") or request.headers.get(
        "X-User-Id"
    )
    if not admin_user_id:
        return False

    try:
        admin_user_id = int(admin_user_id)
    except (TypeError, ValueError):
        return False

    return users.objects.filter(id=admin_user_id, role="admin", is_active=True).exists()


def _admin_forbidden_response():
    return JsonResponse(
        {"detail": "Admin access required."},
        status=403,
    )


@require_http_methods(["GET"])
def root(request):
    return JsonResponse(
        {
            "message": "RealEstate Admin API",
            "endpoints": [
                "/admin/users",
                "/admin/users/{id}/block",
                "/admin/properties",
                "/admin/properties/{id}/approve",
                "/admin/properties/{id}/reject",
            ],
        }
    )


@csrf_exempt
@require_http_methods(["GET"])
def admin_list_users(request):
    if not _is_admin_request(request):
        return _admin_forbidden_response()

    fields = [
        "id",
        "email",
        "phone",
        "role",
        "full_name",
        "is_verified",
        "is_active",
        "created_at",
        "updated_at",
    ]
    all_users = users.objects.all().values(*fields)
    return JsonResponse(list(all_users), safe=False)


@csrf_exempt
@require_http_methods(["PATCH"])
def admin_block_user(request, id):
    if not _is_admin_request(request):
        return _admin_forbidden_response()

    user = get_object_or_404(users, id=id)
    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])
    return JsonResponse({"message": "User blocked successfully"})


@csrf_exempt
@require_http_methods(["GET"])
def admin_list_properties(request):
    if not _is_admin_request(request):
        return _admin_forbidden_response()

    fields = [
        "id",
        "owner_id",
        "title",
        "description",
        "price",
        "listing_type",
        "property_type",
        "bedrooms",
        "bathrooms",
        "area_sqft",
        "city",
        "state",
        "country",
        "pincode",
        "status",
        "is_featured",
        "created_at",
        "updated_at",
    ]
    all_properties = properties.objects.all().values(*fields)
    return JsonResponse(list(all_properties), safe=False)


@csrf_exempt
@require_http_methods(["PATCH"])
def admin_approve_property(request, id):
    if not _is_admin_request(request):
        return _admin_forbidden_response()

    property_obj = get_object_or_404(properties, id=id)
    property_obj.status = "approved"
    property_obj.save(update_fields=["status", "updated_at"])
    return JsonResponse({"message": "Property approved"})


@csrf_exempt
@require_http_methods(["PATCH"])
def admin_reject_property(request, id):
    if not _is_admin_request(request):
        return _admin_forbidden_response()

    property_obj = get_object_or_404(properties, id=id)
    property_obj.status = "rejected"
    property_obj.save(update_fields=["status", "updated_at"])
    return JsonResponse({"message": "Property rejected"})

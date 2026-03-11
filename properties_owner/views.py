import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import User


def _serialize_user(user_obj):
	return {
		"id": str(user_obj.id),
		"name": user_obj.name,
		"email": user_obj.email,
		"phone": user_obj.phone,
		"is_active": user_obj.is_active,
		"created_at": (
			user_obj.created_at.isoformat() if user_obj.created_at is not None else None
		),
		"updated_at": (
			user_obj.updated_at.isoformat() if user_obj.updated_at is not None else None
		),
	}


def _read_payload(request):
	try:
		payload = json.loads(request.body.decode("utf-8") or "{}")
	except (json.JSONDecodeError, UnicodeDecodeError):
		payload = {}

	if not payload:
		payload = request.POST.dict()

	return payload


@require_http_methods(["POST"])
def create_user(request):
	payload = _read_payload(request)

	missing_fields = [field for field in ["name", "email"] if not payload.get(field)]
	if missing_fields:
		return JsonResponse(
			{
				"success": False,
				"message": "Missing required fields.",
				"missing_fields": missing_fields,
			},
			status=400,
		)

	now = timezone.now()
	try:
		user_obj = User.objects.create(
			name=payload["name"],
			email=payload["email"],
			phone=payload.get("phone"),
			is_active=payload.get("is_active", True),
			created_at=now,
			updated_at=now,
		)
	except IntegrityError:
		return JsonResponse(
			{
				"success": False,
				"message": "A user with this email already exists.",
			},
			status=400,
		)

	return JsonResponse(
		{
			"success": True,
			"message": "User created successfully.",
			"user": _serialize_user(user_obj),
		},
		status=201,
	)


@require_http_methods(["GET"])
def list_users(request):
	queryset = User.objects.all().order_by("-created_at")

	data = [_serialize_user(user_obj) for user_obj in queryset]
	return JsonResponse({"success": True, "count": len(data), "results": data}, status=200)


@require_http_methods(["GET"])
def user_detail(request, id):
	try:
		user_obj = User.objects.get(pk=id)
	except User.DoesNotExist:
		return JsonResponse({"success": False, "message": "User not found."}, status=404)

	return JsonResponse({"success": True, "user": _serialize_user(user_obj)}, status=200)


@require_http_methods(["PUT", "PATCH", "POST"])
def update_user(request, id):
	try:
		user_obj = User.objects.get(pk=id)
	except User.DoesNotExist:
		return JsonResponse({"success": False, "message": "User not found."}, status=404)

	payload = _read_payload(request)
	updatable_fields = ["name", "email", "phone", "is_active"]

	for field in updatable_fields:
		if field in payload:
			setattr(user_obj, field, payload[field])

	user_obj.updated_at = timezone.now()
	try:
		user_obj.save()
	except IntegrityError:
		return JsonResponse(
			{
				"success": False,
				"message": "A user with this email already exists.",
			},
			status=400,
		)

	return JsonResponse(
		{
			"success": True,
			"message": "User updated successfully.",
			"user": _serialize_user(user_obj),
		},
		status=200,
	)


@require_http_methods(["DELETE", "POST"])
def delete_user(request, id):
	try:
		user_obj = User.objects.get(pk=id)
	except User.DoesNotExist:
		return JsonResponse({"success": False, "message": "User not found."}, status=404)

	user_obj.delete()

	return JsonResponse(
		{"success": True, "message": "User deleted successfully."},
		status=200,
	)

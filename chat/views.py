from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .services import chatbot_reply


@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot_api(request):

    if not request.data:
        return Response({"error": "No JSON data sent"}, status=400)

    message = request.data.get("message")

    if not message:
        return Response({"error": "Message field required"}, status=400)

    response = chatbot_reply(request.user, message)

    return Response(response)
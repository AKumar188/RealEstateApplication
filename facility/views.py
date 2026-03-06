from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Facility
from .serializers import FacilitySerializer


class FacilityListView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		facilities = Facility.objects.filter(is_active=True).order_by("facility_name")
		serializer = FacilitySerializer(facilities, many=True)
		return Response(serializer.data)

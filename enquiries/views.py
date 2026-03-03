from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Enquiry
from .serializers import EnquirySerializer
from properties.models import Property


class CreateInquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        property_obj = get_object_or_404(Property, id=id)

        enquiry = Enquiry.objects.create(
            property=property_obj,
            sender=request.user,
            owner=property_obj.owner,  # assuming Property has owner field
            message=request.data.get("message"),
            status="pending"
        )

        serializer = EnquirySerializer(enquiry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyInquiriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        property_obj = get_object_or_404(Property, id=id)

        # Only owner can see
        if property_obj.owner != request.user:
            return Response({"error": "Not allowed"}, status=403)

        enquiries = Enquiry.objects.filter(property=property_obj)
        serializer = EnquirySerializer(enquiries, many=True)
        return Response(serializer.data)


class MyInquiriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enquiries = Enquiry.objects.filter(sender=request.user)
        serializer = EnquirySerializer(enquiries, many=True)
        return Response(serializer.data)
# Create your views here.

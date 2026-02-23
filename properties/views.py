from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer


# ✅ CREATE PROPERTY
@api_view(['POST'])
def create_property(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ LIST + SEARCH
@api_view(['GET'])
def search_properties(request):
    properties = Property.objects.all()

    city = request.GET.get('city')
    state = request.GET.get('state')

    if city:
        properties = properties.filter(city__iexact=city)

    if state:
        properties = properties.filter(state__iexact=state)

    serializer = PropertySerializer(properties, many=True)

    return Response({
        "total": properties.count(),
        "results": serializer.data
    })


# ✅ DETAIL
@api_view(['GET'])
def property_detail(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PropertySerializer(property)
    return Response(serializer.data)


# ✅ UPDATE
@api_view(['PUT'])
def update_property(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PropertySerializer(property, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ DELETE
@api_view(['DELETE'])
def delete_property(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    property.delete()
    return Response({"message": "Deleted successfully"})


# ✅ MY LISTINGS (for now same as all)
@api_view(['GET'])
def my_listings(request):
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)
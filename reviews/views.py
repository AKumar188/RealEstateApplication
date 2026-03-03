from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer


# Create Review + Get All Reviews
class ReviewListCreateAPI(APIView):

    def get(self, request):
        property_id = request.GET.get('property_id')

        if property_id:
            reviews = Review.objects.filter(property=property_id)
        else:
            reviews = Review.objects.all()

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Get Single Review + Update + Delete
class ReviewDetailAPI(APIView):

    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None


    def get(self, request, id):
        review = self.get_object(id)

        if not review:
            return Response({"error": "Review not found"})

        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def put(self, request, id):
        review = self.get_object(id)

        if not review:
            return Response({"error": "Review not found"})

        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    def delete(self, request, id):
        review = self.get_object(id)

        if not review:
            return Response({"error": "Review not found"})

        review.delete()

        return Response({"message": "Review deleted"})
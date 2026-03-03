from django.urls import path
from .views import CreateInquiryView, PropertyInquiriesView, MyInquiriesView

urlpatterns = [
    path('create/<uuid:id>/', CreateInquiryView.as_view(), name='create-inquiry'),
    path('property/<uuid:id>/', PropertyInquiriesView.as_view(), name='property-inquiries'),
    path('my/', MyInquiriesView.as_view(), name='my-inquiries'),
]
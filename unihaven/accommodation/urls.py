# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accommodation.views import OwnerViewSet, AccommodationViewSet, ReservationViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'owners', OwnerViewSet)
router.register(r'accommodations', AccommodationViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
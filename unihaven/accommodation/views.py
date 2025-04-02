from django.shortcuts import render

# Create your views here.

# accommodation/views.py

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

from .models import Owner, Accommodation, Reservation, Rating
from .serializers import OwnerSerializer, AccommodationSerializer, ReservationSerializer, RatingSerializer
from .utils import calculate_distance, get_campus_coordinates

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'beds', 'bedrooms', 'created_at']
    
    def get_queryset(self):
        queryset = Accommodation.objects.all()
        
        # Apply filters from query parameters
        accommodation_type = self.request.query_params.get('type')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_beds = self.request.query_params.get('min_beds')
        min_bedrooms = self.request.query_params.get('min_bedrooms')
        
        if accommodation_type:
            queryset = queryset.filter(type=accommodation_type)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_beds:
            queryset = queryset.filter(beds__gte=min_beds)
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)
            
        # Handle distance filtering
        near_campus = self.request.query_params.get('near_campus')
        max_distance = self.request.query_params.get('max_distance')
        
        if near_campus and max_distance:
            campus = get_campus_coordinates(near_campus)
            
            if not campus:
                return queryset
            
            # Convert queryset to list to manipulate
            accommodations = list(queryset)
            
            # Calculate distances
            for accommodation in accommodations:
                accommodation.distance = calculate_distance(
                    campus, 
                    (accommodation.latitude, accommodation.longitude)
                )
            
            # Filter by distance
            accommodations = [a for a in accommodations if a.distance <= float(max_distance)]
            
            # Sort by distance
            accommodations.sort(key=lambda a: a.distance)
            
            return accommodations
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Check if building name is provided
        building_name = request.data.get('building_name')
        
        if building_name:
            # Get address info from DATA.GOV.HK
            address_info = get_address_info(building_name)
            
            if address_info:
                # Add the location data to the request data
                request.data['latitude'] = address_info['latitude']
                request.data['longitude'] = address_info['longitude']
                request.data['geo_address'] = address_info['geo_address']
        
        # Continue with normal creation process
        return super().create(request, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def create(self, request, *args, **kwargs):
        # Add validation logic if needed
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'status': 'reservation cancelled'})

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def create(self, request, *args, **kwargs):
        # Ensure user can only rate after the end of contract
        # This would require additional logic with real dates
        return super().create(request, *args, **kwargs)

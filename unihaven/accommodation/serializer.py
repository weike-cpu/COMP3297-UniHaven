# accommodation/serializers.py

from rest_framework import serializers
from .models import Owner, Accommodation, Reservation, Rating

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'name', 'contact']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user_id', 'score', 'comment', 'created_at']

class AccommodationSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Owner.objects.all(), 
        source='owner', 
        write_only=True
    )
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Accommodation
        fields = [
            'id', 'title', 'description', 'type', 'price', 
            'beds', 'bedrooms', 'latitude', 'longitude', 'geo_address',
            'available_from', 'available_until', 'owner', 'owner_id',
            'average_rating', 'created_at'
        ]
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if not ratings:
            return None
        return sum(r.score for r in ratings) / len(ratings)

class ReservationSerializer(serializers.ModelSerializer):
    accommodation = AccommodationSerializer(read_only=True)
    accommodation_id = serializers.PrimaryKeyRelatedField(
        queryset=Accommodation.objects.all(),
        source='accommodation',
        write_only=True
    )
    
    class Meta:
        model = Reservation
        fields = ['id', 'accommodation', 'accommodation_id', 'user_id', 'status', 'created_at']
from django.db import models

# Create your models here.
class Owner(models.Model): #owner for the accommodation (done)
    CONTACT_TYPES =[
        ('ema', 'Email'),
        ('pho', 'Phone number')
    ]
    name = models.CharField(max_length=100)
    contact_method = models.CharField(
        max_length=3,
        choices=CONTACT_TYPES,
        default="pho"
    )
    contact_info = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Location(models.Model): #store the building location and numbers (done)
    building_name = models.CharField(max_length=200)
    building_location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    #many to many to campus
    
    def __str__(self):
        return self.building_name

class Accommodation(models.Model): #accommodation details （done)
    ACCOMMODATION_TYPES = [
        ('apa', 'Apartment'),
        ('hou', 'House'),
        ('srm', 'Single Room'),
        ('mrm', 'Shared Room'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(
        max_length=3,
        choices=ACCOMMODATION_TYPES,
        default="apa"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    detail_address = models.CharField(max_length=200) #floor and flat
    available_from = models.DateField()
    available_until = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='accommodations')
    #One owner has many accommodation (Parent to Owner)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='accommodations')
    #One location has many accommodation (Parent to Location)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Campus(models.Model): #store campus (done)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    location = models.ManyToManyField(Location, through='CampusDistance')
    def __str__(self):
        return self.name
    
class CampusDistance(models.Model): #Store the Campus Distance for location and campus (midpoint) (done)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)   
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    distance_km = models.FloatField()
    
    def __str__(self):
        return f'Between {self.campus.name} and {self.location.building_name}'
    
class Member(models.Model): #HKU member for reservation (done)
    CONTACT_TYPES =[
        ('ema', 'Email'),
        ('pho', 'Phone number')
    ]
    name = models.CharField(max_length=100)
    contact_method = models.CharField(
        max_length=3,
        choices=CONTACT_TYPES,
        default="pho"
    )
    contact_info = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Reservation(models.Model): #reservation for the accomodation (done)
    STATUS_CHOICES = [
        ('pen', 'Pending'),
        ('fir', 'Confirmed'),
        ('Cel', 'Cancelled'),
    ]
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reservations')
    #One accommodation has many reservations (Parent to accommodation)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pen')
    created_at = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservatioins')
    #One member has many reservation (Parent to Member)

    def __str__(self):
        return f"Reservation for {self.accommodation.title} by {self.user_id}"
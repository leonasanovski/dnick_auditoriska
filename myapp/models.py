from django.contrib.auth.models import User
from django.db import models
"""
username:admin
email:admin@gmail.com
password:admin
"""
# Create your models here.
class FlightCompany(models.Model):
    company_name = models.CharField(max_length=100)
    year_of_establishment = models.IntegerField()
    is_europe_only = models.BooleanField()
    def __str__(self):
        return f'{self.company_name} - {self.year_of_establishment}'
class FlightCompanyLog(models.Model):
    name_of_company = models.CharField(max_length=100)
    total_flights = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return f'{self.name_of_company} log'

class Balloon(models.Model):
    BALLOON_TYPE_CHOICES = [
        ("L","Large"),
        ("M","Medium"),
        ("S","Small"),
    ]
    balloon_type = models.CharField(max_length=1, choices=BALLOON_TYPE_CHOICES)
    manufacturer = models.CharField(max_length=100)
    maximum_capacity = models.IntegerField()
    def __str__(self):
        return f"created by {self.manufacturer} with max.capacity of {self.maximum_capacity} passengers"

class Pilot(models.Model):
    PILOT_RANK_CHOICES = [
        ("B","Beginner"),
        ("I","Intermediate"),
        ("E","Expert"),
    ]
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    year_of_birth = models.IntegerField()
    total_hours_on_flight = models.DecimalField(max_digits=5, decimal_places=1)
    rank_in_company = models.CharField(max_length=1, choices=PILOT_RANK_CHOICES)
    def __str__(self):
        return f'{self.name} {self.surname}'

class Flight(models.Model):
    code = models.CharField(max_length=10, unique=True)
    departure_airport = models.CharField(max_length=50, unique=True)
    landing_airport = models.CharField(max_length=50, unique=True)
    user_that_created = models.ForeignKey(User, on_delete=models.CASCADE)
    """
    for the ImageField options:
    upload_to - where the images are stored
        if the image is flight_1.png --> then it will be stored in 'media/flight_images/flight_1.opg'
    null=True - means that in the database is not required to have some info, it can be null
        (if the field is not null=True, it will be taken as REQUIRED)
    blank=True - means that the user is allowed not to put an image in the form of creating
    """
    flight_image = models.ImageField(upload_to='flights/',null=True, blank=True)
    flight_company = models.ForeignKey(FlightCompany, on_delete=models.CASCADE)
    balloon = models.ForeignKey(Balloon, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.code} - from {self.departure_airport} to {self.landing_airport}'

class AirCompanyPilot(models.Model):
    company = models.ForeignKey(FlightCompany, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
class FlightReport(models.Model):
    flight_instance = models.ForeignKey(Flight, on_delete=models.CASCADE)
    description = models.TextField()
    def __str__(self):
        return f'- {self.flight_instance.code} -'
class Product(models.Model):
    #charfield
    name = models.CharField(max_length=100)
    #textfield
    description = models.TextField()
    #decimalfield
    price = models.DecimalField(max_digits=6, decimal_places=2)
    #max format looks like this -> xxxx.xx
    #booleanfield
    in_stock = models.BooleanField(default=True)
    #DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp on creation
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp on every update
    #imagefield
    image = models.ImageField(upload_to='path/', height_field=None, width_field=None)
    #integerfield
    year_of_establishment = models.IntegerField()
    #choicesfield

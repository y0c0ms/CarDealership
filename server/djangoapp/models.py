from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# CarMake model to save data about a car's make
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Any other fields you would like to include in car make model
    
    def __str__(self):
        return self.name  # Return the name as the string representation


# CarModel model to save data about a car's model
class CarModel(models.Model):
    # Many-To-One relationship to Car Make model (One Car Make has many Car Models)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    # Dealer Id refers to a dealer created in Cloudant database
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    # Type with limited choices
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')
    # Year with min value 2015 and max value 2023
    year = models.IntegerField(default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ])
    # Any other fields you would like to include in car model
    
    def __str__(self):
        return f"{self.car_make.name} {self.name}"  # Return the car make and model name

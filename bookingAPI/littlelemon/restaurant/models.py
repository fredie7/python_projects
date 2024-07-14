from django.db import models

# Create the models.

class Booking(models.Model):
    
    # Define features
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)    
    no_of_guests = models.IntegerField()
    bookingDate = models.DateTimeField()

    def __str__(self):
        return self.name

class Menu(models.Model):
    
    # Define features

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.BigIntegerField()

    def __str__(self):
        return f'{self.title} : {str(self.price)}'
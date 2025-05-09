from django.db import models
from signup.models import User  # Use your custom User model

class RoomType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Room(models.Model):
    FLOOR_CHOICES = [
        ('1', 'First Floor - A'),
        ('2', 'Second Floor - B'),
        ('3', 'Third Floor - C'),
        ('4', 'Fourth Floor - D'),
        ('5', 'Fifth Floor - E'),
    ]

    room_number = models.CharField(max_length=3)  # A1, B2, etc.
    floor = models.CharField(max_length=1, choices=FLOOR_CHOICES)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number}"

    class Meta:
        unique_together = ['room_number', 'floor']

class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    
    user = models.ForeignKey('signup.User', on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    # Payment status field
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Informations sur le client
    guest_first_name = models.CharField(max_length=100)
    guest_last_name = models.CharField(max_length=100)
    guest_gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    guest_phone = models.CharField(max_length=20)
    guest_email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.room.room_number} by {self.guest_first_name} {self.guest_last_name}"

    class Meta:
        ordering = ['-booking_date']

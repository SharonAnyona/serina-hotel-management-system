from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

from accounts.models import Employee

# Create your models here.


class Room(models.Model):
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),

    )
    number = models.IntegerField(primary_key=True)
    capacity = models.SmallIntegerField()
    numberOfBeds = models.SmallIntegerField()
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.FloatField()
    statusStartDate = models.DateField(null=True)
    statusEndDate = models.DateField(null=True)

    def __str__(self):
        return str(self.number)
    
class Guest(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber = PhoneNumberField(unique=True)

    def __str__(self):
        return str(self.user)

    def numOfBooking(self):
        return Booking.objects.filter(guest=self).count()

    def numOfDays(self):
        totalDay = 0
        bookings = Booking.objects.filter(guest=self)
        for b in bookings:
            day = b.endDate - b.startDate
            totalDay += int(day.days)

        return totalDay

    def numOfLastBookingDays(self):
        try:
            return int((Booking.objects.filter(guest=self).last().endDate - Booking.objects.filter(guest=self).last().startDate).days)
        except:
            return 0

    def currentRoom(self):
        booking = Booking.objects.filter(guest=self).last()
        return booking.roomNumber


class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def numOfDep(self):
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)


class Dependees(models.Model):
    booking = models.ForeignKey(Booking,   null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def str(self):
        return str(self.booking) + " " + str(self.name)


class Refund(models.Model):
    guest = models.ForeignKey(Guest,   null=True, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return str(self.guest)

class FoodMenu(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    menuItems = models.TextField()

    def __str__(self):
        return str(self.menuItems) + " " + str(self.startDate)


class RoomServices(models.Model):
    SERVICES_TYPES = (
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning'),
        ('Technical', 'Technical'),
    )

    curBooking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    createdDate = models.DateField(default=timezone.now)
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES)
    price = models.FloatField()
    foodMenu = models.ForeignKey(FoodMenu, null=True, blank=True, on_delete=models.CASCADE)  # New field for food menu

    def __str__(self):
        return f"{self.curBooking} {self.room} {self.servicesType}"

class Task(models.Model):
    employee = models.ForeignKey(
        Employee,   null=True, on_delete=models.CASCADE)
    room_service = models.ForeignKey(RoomServices, null=True, blank=True, on_delete=models.SET_NULL)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField()

    def str(self):
        return str(self.employee)
    

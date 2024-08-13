from django.db import models
from django.conf import settings
from account.models import Myuser

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hall(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(default=0)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    services = models.ManyToManyField(Service)
    manager = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    total_seats = models.PositiveIntegerField()
    booked_seats = models.PositiveIntegerField(default=0)
    available_seats = models.PositiveIntegerField()
    working_hours = models.JSONField(default=dict)
    image = models.ImageField(upload_to='halls/', default='halls/default.jpg')
    
    def save(self, *args, **kwargs):
        self.available_seats = self.total_seats - self.booked_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    bell = models.DecimalField(max_digits=4, decimal_places=2,blank=True)
    number_of_seats = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=4, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.bell:
            duration_in_hours = (self.end_time - self.start_time).total_seconds() / 3600
            self.bell = Decimal(duration_in_hours) * self.price_per_hour * Decimal(self.number_of_seats)

        self.hall.booked_seats += self.number_of_seats
        self.hall.save()
        super().save(*args, **kwargs)

class Review(models.Model):
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.hall.name}"
    
class Replay(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='replay')
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replay by {self.user.username} to review {self.review.id}"

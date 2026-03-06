from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Dish(models.Model):
    image = models.ImageField(upload_to='dishes/')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.name
class Offer(models.Model):
    image=models.ImageField(upload_to='offers/')
    name=models.CharField(max_length=20)   
    percentage=models.PositiveIntegerField()
    code=models.CharField(max_length=10)
    def __str__(self):
        return f"{self.title}({self.code})"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ("Placed","Placed"),
        ("Cancelled","Cancelled"),
        ("Preparing","Preparing"),
        ("Delivered","Delivered"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Placed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} ({self.status})"

    def can_cancel(self):
        """Allow cancel only if within 10 minutes and still Placed."""
        return (
            self.status == "Placed"
            and timezone.now() - self.created_at <= timedelta(minutes=10)
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
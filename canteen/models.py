from django.db import models
from django.contrib.auth.models import User


class FoodItem(models.Model):

    name = models.CharField(max_length=100)

    price = models.IntegerField()

    description = models.TextField()
    image = models.ImageField(upload_to='food_images/')   # ADD THIS
    available = models.BooleanField(default=True)


    def __str__(self):

        return self.name




class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)


    def __str__(self):

        return f"{self.user.username} - {self.food.name}"




class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    status = models.CharField(max_length=50, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f"{self.user.username} - {self.food.name}"
    
class OTP(models.Model):

    email = models.EmailField()

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f"{self.email} - {self.otp}"
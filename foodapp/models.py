from django.db import models
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.category_name



class FoodItem(models.Model):
    food_name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to='food_images/',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"

    def __str__(self):
        return self.food_name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.food.food_name}"


class Order(models.Model):

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        default='Order Placed'
    )

    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    food = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

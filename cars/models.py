from django.db import models
from brands.models import Brand
from django.contrib.auth.models import User
# Create your models here.


class Car(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,  null=True, blank=True)
    
    l_user = models.ForeignKey(User, on_delete=models.CASCADE) 
    Price = models.FloatField( blank=True, null=True)  
    Available = models.IntegerField(default=0)  
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.title 
    class Meta:
        unique_together = ('title', 'brand')
    
    def decrease_available(self):
        if self.Available > 0:
            self.Available -= 1
            self.save()


class Comment(models.Model):
    car= models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models. TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"
    


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.car.title} - {self.quantity}"
from django.utils.timezone import now
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(blank=True, null=True)  # Automatically set from Car's Price
    timestamp = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.price:  # Set the price only if it's not already set
            self.price = self.car.Price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car.title} - {self.quantity} @ {self.price}"

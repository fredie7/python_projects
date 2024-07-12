from django.db import models
from django.contrib.auth.models import User

# Create models.

# Model for item categories
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=200, db_index=True)

# Model for singular item on the menu, linking the Category model
class MenuItem(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

# Model for item cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unitPrice = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menuItem')

# # Model for the order
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     deliveryCrew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='deliveryCrew', null=True)
#     status = models.BooleanField(db_index=True, default=0)
#     total = models.DecimalField(max_digits=6,decimal_places=2)
#     date = models.DateField(db_index=True)

# # Model for singular order along with associated links with the Order and MenuItem table
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     unitPrice = models.DecimalField(max_digits=6, decimal_places=2)
#     price = models.DecimalField(max_digits=6, decimal_places=2)

#     class Meta:
#         unique_together = ('order', 'menuItem')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deliveryCrew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="deliveryCrew", null=True)
    status = models.BooleanField(default=0, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date = models.DateField(db_index=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order')
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuItem')
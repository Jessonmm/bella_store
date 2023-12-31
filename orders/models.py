from django.db import models
from accounts.models import Account
from shop.models import *
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=550)
    last_name = models.CharField(max_length=550)
    email = models.EmailField(max_length=550)
    phone_number = models.CharField(max_length=515)
    address_line1 = models.CharField(max_length=550,  null=True)
    address_line2 = models.CharField(max_length=550, null=True)
    country  = models.CharField(max_length=550)
    state = models.CharField(max_length=550)
    district = models.CharField(max_length=550)
    city = models.CharField(max_length=550, blank=True)
    pincode = models.IntegerField(default=0)
    order_note = models.CharField(max_length=100, blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def address(self):
        return f"{self.address_line1} {self.address_line2}"

    def __str__(self):
        return self.first_name


class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,unique=True)
    order_id = models.CharField(max_length=100,blank=True,unique=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)



class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', "Sf`hipped"),
        ('Out for delivery', "Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=50, default='')
    address_line1 = models.CharField(max_length=50, default='')
    address_line2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    district = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    pincode = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    full_price = models.IntegerField(default=0)
    order_discount = models.IntegerField(default=0)
    tax = models.IntegerField()
    shipping = models.IntegerField()


    status = models.CharField(max_length=50, choices=STATUS, default='Order Confirmed')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    return_reason = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='user_order_page')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        return round(int(self.product_price) * int(self.quantity))

class Coupons(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)])
    min_value = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_at = models.DateField()
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.code


class UserCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_coupon')
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Wallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"wallet for {self.user.username}"


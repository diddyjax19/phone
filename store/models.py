from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Product model
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=200, verbose_name="Nearest Location")
    city = models.CharField(max_length=200, verbose_name="City")
    state = models.CharField(max_length=200, verbose_name="State")

    def __str__(self):
        return self.locality


#Category model 
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Category Title")
    slug = models.SlugField(max_length=50, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        # order categories according to date created
        ordering = ('-created_at', )

    # return string representation of the model
    def __str__(self):
        return self.title


# Product model
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Product Title")
    slug = models.SlugField(max_length=155, verbose_name="Product Slug")
    sku = models.CharField(max_length=155, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        # order products according to date created
        ordering = ('-created_at', )

    # return string representation of the model
    def __str__(self):
        return self.title


# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    # return string representation of the model
    def __str__(self):
        return str(self.user)
    
    # Creating Model Property to calculate total price (Quantity x Price)
    @property
    def total_price(self):
        return self.quantity * self.product.price


# order status
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


#Order model 
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        default="Pending"
        )

# Coupon model 
# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True)
#     value = models.IntegerField()
#     active = models.BooleanField(default=True)
#     num_available = models.IntegerField(default=1)
#     num_used = models.IntegerField(default=0)

#     def __str__(self):
#         return self.code
    
#     def can_use(self):
#         is_active = True

#         if self.active == False:
#             is_active = False
        
#         if self.num_used >= self.num_available and self.num_available != 0:
#             is_active = False
        
#         return is_active
    
#     def use(self):
#         self.num_used = self.num_used + 1

#         if self.num_used == self.num_available:
#             self.active = False
        
#         self.save()
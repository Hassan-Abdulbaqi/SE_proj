from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, username, mobile_number, password=None, **extra_fields):
        """Create and save a regular user"""
        if not username:
            raise ValueError('Users must have a username')
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        
        email = extra_fields.get('email', '')
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            username=username,
            mobile_number=mobile_number,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, mobile_number, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, mobile_number, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with mobile number"""
    mobile_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    
    objects = UserManager()
    
    def __str__(self):
        return self.username


class Service(models.Model):
    """Service types: Electricity, Water, Gas"""
    SERVICE_TYPES = [
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, unique=True)
    name_ar = models.CharField(max_length=100)  # Arabic name
    name_en = models.CharField(max_length=100)  # English name
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per kWh/Liter/m³
    unit_name = models.CharField(max_length=50)  # kWh, Liter, m³
    unit_name_ar = models.CharField(max_length=50)  # Arabic unit name
    
    def __str__(self):
        return f"{self.name_en} ({self.service_type})"


class Order(models.Model):
    """Order model"""
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Number of units (kWh, Liters, m³)
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of service
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Delivery cost
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Total cost
    location = models.TextField()  # Delivery location
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    notes = models.TextField(blank=True, null=True)  # Special notes
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    estimated_delivery_time = models.IntegerField(default=60)  # Estimated delivery time in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.service.name_en}"
    
    class Meta:
        ordering = ['-created_at']


class OrderTracking(models.Model):
    """Order tracking information"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    remaining_delivery_time = models.IntegerField()  # Remaining time in minutes
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Tracking for Order #{self.order.id}"


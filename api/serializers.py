from decimal import Decimal

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Service, Order, OrderTracking


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class SignUpSerializer(serializers.ModelSerializer):
    """Sign up serializer - no password validation for dev mode"""
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'mobile_number', 'password', 'password_confirm', 'email']
        extra_kwargs = {
            'email': {'required': False},
        }
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user


class SignInSerializer(serializers.Serializer):
    """Sign in serializer"""
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')
        
        if not mobile_number or not password:
            raise serializers.ValidationError("Must include mobile_number and password")
        
        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist (security best practice)
            # But for development, we can be more helpful
            raise serializers.ValidationError({
                "mobile_number": f"No account found with mobile number {mobile_number}. Please sign up first."
            })
        
        if not user.check_password(password):
            raise serializers.ValidationError({
                "password": "Incorrect password. Please try again."
            })
        
        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")
        
        attrs['user'] = user
        return attrs


class ServiceSerializer(serializers.ModelSerializer):
    """Service serializer"""
    currency = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id',
            'service_type',
            'name_ar',
            'name_en',
            'price_per_unit',
            'unit_name',
            'unit_name_ar',
            'currency',
        ]

    def get_currency(self, obj):
        return getattr(settings, 'DEFAULT_CURRENCY', 'IQD')


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer"""
    service = ServiceSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    currency = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'service', 'service_id', 'quantity', 'service_cost',
            'delivery_cost', 'total_cost', 'location', 'payment_method', 'currency',
            'notes', 'status', 'estimated_delivery_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_currency(self, obj):
        return getattr(settings, 'DEFAULT_CURRENCY', 'IQD')


class OrderTrackingSerializer(serializers.ModelSerializer):
    """Order tracking serializer"""
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = OrderTracking
        fields = ['id', 'order', 'remaining_delivery_time', 'last_updated']
        read_only_fields = ['id', 'last_updated']


class CheckoutSerializer(serializers.Serializer):
    """Checkout serializer"""
    service_id = serializers.IntegerField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    location = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=['cash', 'card'])
    notes = serializers.CharField(required=False, allow_blank=True)
    delivery_cost = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0'),
        default=0,
        required=False
    )
    estimated_delivery_time = serializers.IntegerField(default=60)


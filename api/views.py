from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderTracking, Service, User
from .serializers import (
    UserSerializer, SignUpSerializer, SignInSerializer,
    ServiceSerializer, OrderSerializer, OrderTrackingSerializer,
    CheckoutSerializer
)

TWO_PLACES = Decimal('0.01')
DEFAULT_CURRENCY = getattr(settings, 'DEFAULT_CURRENCY', 'IQD')


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """User signup endpoint"""
    from django.contrib.auth import authenticate
    
    print(f"[DEBUG] Signup request data: {request.data}")
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Authenticate the user to set the backend attribute
        authenticated_user = authenticate(
            request,
            mobile_number=user.mobile_number,
            password=request.data.get('password')
        )
        if authenticated_user:
            login(request, authenticated_user)
        else:
            # Fallback: manually set backend and login
            user.backend = 'api.backends.MobileNumberBackend'
            login(request, user)
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    print(f"[DEBUG] Signup validation errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    """User signin endpoint"""
    from django.contrib.auth import authenticate
    
    print(f"[DEBUG] Signin request data: {request.data}")
    mobile_number = request.data.get('mobile_number')
    password = request.data.get('password')
    
    if not mobile_number or not password:
        return Response({
            'error': 'Mobile number and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Use authenticate() which handles multiple backends correctly
    user = authenticate(request, mobile_number=mobile_number, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'This account has been disabled'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Check if user exists to give better error message
        try:
            User.objects.get(mobile_number=mobile_number)
            return Response({
                'error': 'Incorrect password. Please try again.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'error': f'No account found with mobile number {mobile_number}. Please sign up first.'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signout(request):
    """Log the current user out"""
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token(request):
    """Development placeholder - CSRF protection is disabled."""
    return Response({
        'csrfToken': None,
        'message': 'CSRF checks are disabled in development mode.',
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def debug_users(request):
    """Development only - list all users (DO NOT USE IN PRODUCTION!)"""
    if not settings.DEBUG:
        return Response({'error': 'This endpoint is only available in debug mode'}, status=403)
    
    users = User.objects.all()
    user_list = [
        {
            'id': user.id,
            'username': user.username,
            'mobile_number': user.mobile_number,
            'email': user.email,
        }
        for user in users
    ]
    return Response({
        'total_users': users.count(),
        'users': user_list,
        'warning': 'This endpoint should NEVER be used in production!'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Get user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({
            'error': 'old_password and new_password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not request.user.check_password(old_password):
        return Response({
            'error': 'Invalid old password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.set_password(new_password)
    request.user.save()
    return Response({'message': 'Password changed successfully'})


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Service viewset - read only"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def calculate_cost(self, request):
        """Calculate cost for a service"""
        service_id = request.query_params.get('service_id')
        quantity = request.query_params.get('quantity')
        
        if not service_id or not quantity:
            return Response({
                'error': 'service_id and quantity are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = Service.objects.get(id=service_id)
            quantity_decimal = Decimal(quantity).quantize(TWO_PLACES)
            cost = (service.price_per_unit * quantity_decimal).quantize(TWO_PLACES)
            
            return Response({
                'service': ServiceSerializer(service).data,
                'quantity': quantity_decimal,
                'cost': cost,
                'currency': DEFAULT_CURRENCY,
            })
        except Service.DoesNotExist:
            return Response({
                'error': 'Service not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except (InvalidOperation, ValueError):
            return Response({
                'error': 'Invalid quantity'
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    """Order viewset"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return orders for the authenticated user"""
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        """Track an order"""
        try:
            order = self.get_object()
            tracking, created = OrderTracking.objects.get_or_create(
                order=order,
                defaults={'remaining_delivery_time': order.estimated_delivery_time}
            )
            serializer = OrderTrackingSerializer(tracking)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Checkout endpoint - create order"""
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                service = Service.objects.get(id=data['service_id'])
                quantity = data['quantity'].quantize(TWO_PLACES)
                service_cost = (service.price_per_unit * quantity).quantize(TWO_PLACES)
                delivery_cost = Decimal(data.get('delivery_cost', Decimal('0'))).quantize(TWO_PLACES)
                total_cost = (service_cost + delivery_cost).quantize(TWO_PLACES)
                
                order = Order.objects.create(
                    user=request.user,
                    service=service,
                    quantity=quantity,
                    service_cost=service_cost,
                    delivery_cost=delivery_cost,
                    total_cost=total_cost,
                    location=data['location'],
                    payment_method=data['payment_method'],
                    notes=data.get('notes', ''),
                    estimated_delivery_time=data.get('estimated_delivery_time', 60)
                )
                
                # Create tracking entry
                OrderTracking.objects.create(
                    order=order,
                    remaining_delivery_time=order.estimated_delivery_time
                )
                
                return Response({
                    'message': 'Order created successfully',
                    'order': OrderSerializer(order).data
                }, status=status.HTTP_201_CREATED)
            except Service.DoesNotExist:
                return Response({
                    'error': 'Service not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


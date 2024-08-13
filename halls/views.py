from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Hall, Service,Review, Replay,Booking
from .serializers import (
HallCreateSerializer, HallListSerializer, HallManagerHomeSerializer, 
    HallUserSerializer, HallUpdateSerializer, ReviewSerializer, 
    ServiceSerializer, ReplaySerializer,BookingSerializer
)

class HallCreateView(generics.CreateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_manager:
            raise PermissionDenied("Only managers can create halls.")
        serializer.save(manager=self.request.user)

class HallListView(generics.ListAPIView):
    serializer_class = HallListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Hall.objects.all().order_by('-rating')

        max_price = self.request.query_params.get('max_price', None)
        min_rating = self.request.query_params.get('min_rating', None)
        services = self.request.query_params.getlist('services', None)

        if max_price:
            queryset = queryset.filter(price_per_hour__lte=max_price)

        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        if services:
            queryset = queryset.filter(services__id__in=services).distinct()

        return queryset

class HallUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        hall = self.get_object()
        if not request.user.is_manager or hall.manager != request.user:
            raise PermissionDenied("Only managers can update hall details.")
        
        services_ids = request.data.get('services')
        if services_ids:
            services = Service.objects.filter(id__in=services_ids)
            hall.services.set(services)
            hall.save()

        return super().update(request, *args, **kwargs)

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_manager:
            raise PermissionDenied("Only managers can access the list of services.")
        return super().get(request, *args, **kwargs)

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_manager:
            raise PermissionDenied("Managers are not allowed to make bookings.")
        
        hall = serializer.validated_data['hall']
        seats_requested = serializer.validated_data['number_of_seats']

        if hall.available_seats < seats_requested:
            raise PermissionDenied("Not enough seats available.")
        
        serializer.save(user=self.request.user)

class UserHallsView(generics.ListAPIView):
    serializer_class = HallUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Hall.objects.filter(manager=self.request.user)

class ManagerHomeView(generics.ListAPIView):
    serializer_class = HallManagerHomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Hall.objects.filter(manager=self.request.user)

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        hall = serializer.validated_data['hall']
        if Review.objects.filter(user=self.request.user, hall=hall).exists():
            raise PermissionDenied("You have already reviewed this hall.")
        serializer.save(user=self.request.user)

class ReplayCreateView(generics.CreateAPIView):
    queryset = Replay.objects.all()
    serializer_class = ReplaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = serializer.validated_data['review']
        if review.hall.manager != self.request.user:
            raise PermissionDenied("Only the hall manager can reply to reviews.")
        serializer.save(user=self.request.user)


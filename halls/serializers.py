from rest_framework import serializers
from .models import Hall, Service, Review, Replay,Booking

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']

class ReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Replay
        fields = ['id', 'review', 'user', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    replay = ReplaySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'hall', 'rating', 'comment', 'created_at', 'replay']
        read_only_fields = ['user', 'created_at']

class HallUserSerializer(serializers.ModelSerializer):
    # services = ServiceSerializer(many=True, read_only=True)
    services = serializers.StringRelatedField(many=True, read_only=True)
    working_hours = serializers.JSONField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hall
        fields = ['id', 'name', 'location', 'rating', 'price_per_hour', 'services', 'working_hours', 'available_seats', 'image', 'reviews']

class HallManagerHomeSerializer(serializers.ModelSerializer):
    # services = ServiceSerializer(many=True, read_only=True)
    services = serializers.StringRelatedField(many=True, read_only=True)
    working_hours = serializers.JSONField()
    manager_full_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hall
        fields = ['id', 'name', 'location', 'rating', 'price_per_hour', 'services', 'working_hours', 'manager_full_name', 'total_seats', 'booked_seats', 'available_seats', 'image', 'reviews']

    def get_manager_full_name(self, obj):
        return f"{obj.manager.first_name} {obj.manager.last_name}"

class HallCreateSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(many=True, queryset=Service.objects.all())
    working_hours = serializers.JSONField()

    class Meta:
        model = Hall
        fields = ['name', 'location', 'price_per_hour', 'total_seats', 'working_hours', 'services', 'image']

    def create(self, validated_data):
        services_data = validated_data.pop('services')
        hall = Hall.objects.create(**validated_data)
        hall.services.set(services_data)
        return hall

class HallUpdateSerializer(serializers.ModelSerializer):
    working_hours = serializers.JSONField()

    class Meta:
        model = Hall
        fields = ['name', 'location', 'price_per_hour', 'services', 'total_seats', 'working_hours', 'image']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'hall', 'start_time', 'end_time', 'bell', 'number_of_seats']

    def create(self, validated_data):
        hall = validated_data.get('hall')
        number_of_seats = validated_data.get('number_of_seats')

        price_per_hour = hall.price_per_hour
        duration_in_hours = Decimal((validated_data['end_time'] - validated_data['start_time']).total_seconds()) / 3600

        bell = duration_in_hours * price_per_hour * Decimal(number_of_seats)

        validated_data.pop('hall')

        booking = Booking.objects.create(bell=bell, hall=hall, price_per_hour=price_per_hour, **validated_data)
        return booking

class HallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'location', 'rating', 'price_per_hour', 'image']

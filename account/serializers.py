from rest_framework import serializers
from .models import Myuser
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myuser
        fields = ['username', 'email', 'first_name', 'last_name']
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Myuser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        user = Myuser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = Myuser.objects.get(email=value)
        except Myuser.DoesNotExist:
            raise serializers.ValidationError(_("This email address is not associated with any account."))
        return value

    def save(self):
        email = self.validated_data['email']
        user = Myuser.objects.get(email=email)
        # يجب إضافة منطق هنا لإرسال البريد الإلكتروني مع رابط إعادة تعيين كلمة المرور
        reset_link = "http://example.com/reset-password/"  # رابط افتراضي لإعادة تعيين كلمة المرور
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Myuser
        fields = ('old_password', 'new_password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is not correct."))
        return value

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(_("New password must be different from the old password."))
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance



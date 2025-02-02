from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["name", "email", "password", "password2", "mobile"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        print(password)

        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User not found."})

        # Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError({"email": "User account is inactive."})

        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        return user  # Return user object if successful login


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User not found."})

        # Generate Password Reset Token
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Construct Reset URL
        reset_url = f"http://localhost:8000/auth/reset-password/{uidb64}/{token}/"

        # Send Email with Reset Link
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return {"message": "Password reset link sent to your email."}




class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data["uidb64"]).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({"uidb64": "Invalid user ID."})

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        # Hash and save the new password
        user.password = data["new_password"]
        user.save()

        return {"message": "Password has been reset successfully."}

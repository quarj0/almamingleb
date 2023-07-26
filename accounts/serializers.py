from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Favorite, ProfileView, UserProfile, Message
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "email",
            "password",
            "university",
            "gender",
            "profile_picture",
            "basic_information",
            "passions",
            "about_section",
            "gallery",
        )
        extra_kwargs = {"password": {"write_only": True}}



User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "email",
            "password",
            "university",
            "gender",
            "token",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, user):
        return default_token_generator.make_token(user)

    def create(self, validated_data):
        user_profile = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
            university=validated_data.get("university"),
            gender=validated_data.get("gender"),
        )
        return user_profile


class CustomPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        validate_email(email)
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return email

    def send_reset_email(self):
        user = User.objects.get(email=self.validated_data["email"])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uid, token


class CustomChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Invalid old password.")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def change_password(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "user", "favorite_user", "timestamp")


class ProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileView
        fields = ("id", "viewer", "viewed_user", "timestamp")


class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ("id", "username", "email", "auth_token")
        read_only_fields = ("id", "username", "email")

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'

from django.conf import Settings
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Favorite, ProfileView, UserProfile, Message
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.forms import EmailField
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "email",
            "profile_picture",
            "university",
            "basic_information",
            "passions",
            "about_section",
        )
        extra_kwargs = {
            "profile_picture": {"required": False},
            "university": {"required": False},
            "basic_information": {"required": False},
            "passions": {"required": False},
            "about_section": {"required": False},
        }

    def validate_email(self, value):
        domain = value.split('@')[1]
        allowed_domains = ['ucc.edu.gh', 'knust.edu.gh', 'ug.edu.gh']
        if domain not in allowed_domains:
            raise serializers.ValidationError('Invalid email domain.')
        return value

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(username=username, password=password, email=email)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        password = user_data.get("password")
        instance = super().update(instance, validated_data)
        if password:
            instance.user.set_password(password)
            instance.user.save()
        return instance



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
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return access_token, refresh_token

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user_data = validated_data.copy()
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            data["user"] = user
            return data
        raise serializers.ValidationError("Invalid username or password")


class CustomPasswordResetSerializer(serializers.Serializer):
    email = EmailField()

    def validate_email(self, email):
        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        return email

    def save(self):
        # Get the user and generate the password reset token
        user = User.objects.get(email=self.validated_data["email"])
        token = urlsafe_base64_encode(force_bytes(user.pk))
        # Send the password reset email
        subject = _("Password reset")
        message = _(
            "Please click on the following link to reset your password:\n\n"
            "http://localhost:8000/reset-password/{token}/"
        )
        message = message.format(token=token)
        send_mail(subject, message, Settings.EMAIL_HOST_USER, [user.email])


class CustomChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Invalid old password."))
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self):
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

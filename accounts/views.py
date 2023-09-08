from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Favorite, ProfileView, UserProfile, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from .serializers import (
    UserProfileSerializer,
    ProfileViewSerializer,
    FavoriteSerializer,
    CustomChangePasswordSerializer,
    CustomPasswordResetSerializer,
    MessageSerializer, 
    UserRegistrationSerializer
)



User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = User.objects.create_user(
                serializer.validated_data["username"],
                serializer.validated_data["email"],
                serializer.validated_data["password"],
                university=serializer.validated_data.get("university"),
                gender=serializer.validated_data.get("gender"),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = CustomPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid, token = serializer.send_reset_email()
        return Response({"uid": uid, "token": token})


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = CustomChangePasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        if default_token_generator.check_token(user, token):
            serializer.change_password()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid password reset link."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        email = request.session.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        if otp == request.session.get("otp"):
            # Activate the user's account
            user.is_active = True
            user.save()
            # Log the user in
            user = authenticate(request, email=email)
            login(request, user)
            serializer = UserProfileSerializer(user.userprofile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({"message": "Login successful"})
                else:
                    return JsonResponse({"error": "Your account is disabled."}, status=400)
            else:
                return JsonResponse(
                    {"error": "Invalid login details supplied."}, status=400
                )
        except:
            return Response({"Oops!": "Something went wrong when trying to login. \n Please try again later."})
            
    



class CustomChangePasswordView(generics.GenericAPIView):
    serializer_class = CustomChangePasswordSerializer
    
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."})




def search(request):
    if request.method == "POST":
        age = request.POST.get("age")
        university_name = request.POST.get("university_name")
        program = request.POST.get("program")
        username = request.POST.get("username")

        profiles = UserProfile.objects.filter(
            Q(age=age) | Q(age__isnull=True),
            Q(university_name=university_name) | Q(
                university_name__isnull=True),
            Q(program=program) | Q(program__isnull=True),
            Q(username__icontains=username) | Q(username__isnull=True),
        ).select_related("user")

        results = []
        for profile in profiles:
            user = profile.user
            results.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_picture": profile.profile_picture.url
                    if profile.profile_picture
                    else None,
                    "age": profile.age,
                    "university_name": profile.university_name,
                    "basic_information": profile.basic_information,
                    "passions": profile.passions,
                    "about_section": profile.about_section,
                }
            )

        return JsonResponse({"status": "success", "results": results})
    else:
        return JsonResponse({"status": "error"})



class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = UserProfileSerializer.setup_eager_loading(queryset)
        return queryset


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = UserProfileSerializer.setup_eager_loading(queryset)
        return queryset


@login_required
class DeleteAccountView(generics.DestroyAPIView):
    def post(self, request):
        if request.method == "POST":
            password = request.POST.get("password")
            if request.user.check_password(password):
                # Password confirmation successful, proceed with deletion
                request.user.delete()
                return JsonResponse({"success": True})
            else:
                # Incorrect password, return an error response
                return JsonResponse({"success": False, "error": "Incorrect password."})
        else:
            return JsonResponse({"success": False, "error": "Invalid request method."})


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user=user)


class ProfileViewList(generics.ListAPIView):
    serializer_class = ProfileViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProfileView.objects.filter(viewed_by=user)


class FavoriteList(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)


class FavoriteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)


class MessageListView(LoginRequiredMixin, UpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).order_by("-timestamp")
        serializer = self.serializer_class(messages, many=True)
        return JsonResponse(serializer.data, safe=False)

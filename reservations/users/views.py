from .models import User, Profile
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import RegisterSerializer, CustomObtainPairSerializer, ProfileSerializer, ProfileUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .tasks import send_register_confirmation

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_register_confirmation.delay(user.first_name, user.email)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    def get_object(self):
        return generics.get_object_or_404(Profile, account=self.request.user)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "profile"):
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = Profile.objects.create(account=user)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

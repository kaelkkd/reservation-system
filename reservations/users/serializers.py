from .models import User, Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_staff"] = user.is_staff

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "is_staff": self.user.is_staff,
        }

        return data

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.IntegerField(source="profile.id", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields did not match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)

        return user
    
    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        data = super().to_representation(instance)
        data["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data
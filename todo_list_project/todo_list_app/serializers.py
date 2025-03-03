from rest_framework import serializers
from .models import Task
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Ensure user field is read-only

    class Meta:
        model = Task
        fields = '__all__'  # Include all fields

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user  # Assign logged-in user automatically
        return Task.objects.create(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username  # Add username to token payload
        return token

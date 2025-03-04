from rest_framework import serializers
from .models import Task
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)  # ✅ Yeh sirf username return karega

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Task.objects.create(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token





from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

# User serializer for registration (either email or username)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        email = validated_data.get('email', None)
        username = validated_data.get('username', None)
        password = validated_data['password']

        # Ensure either email or username is provided
        if not email and not username:
            raise ValidationError("Either email or username must be provided.")

        # Create user based on which field is provided
        if email and not username:
            username = email  # Use email as username if no username is provided

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return user
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

import re
from rest_framework import serializers
from accounts.models import FriendRequest,User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(max_length=70)

    class Meta:
        model = User
        fields = ['full_name','email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','email']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['id', 'from_user', 'status', 'created_at']

class PendingFriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer( read_only=True)
    status  = serializers.CharField(source="get_status_display")
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'status', 'created_at']

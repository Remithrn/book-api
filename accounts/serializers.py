# accounts/serializers.py
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        label="Password",
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        label="Confirm Password",
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="This email is already registered."
            )
        ],
    )
    username = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        # Check if username is provided; if not, generate one from the email.
        username = validated_data.get("username")
        if not username or username.strip() == "":
            base_username = validated_data["email"].split("@")[0]
            username = base_username
            counter = 1
            # Ensure the generated username is unique.
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            validated_data["username"] = username

        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

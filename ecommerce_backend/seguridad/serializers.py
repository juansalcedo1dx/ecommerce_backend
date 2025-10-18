from rest_framework import serializers
from .models import Usuario, Rol
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'rol']

    def create(self, validated_data):
        user = Usuario.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            rol=validated_data['rol']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        data['user'] = user
        return data

from rest_framework import serializers
from users.models import Department, Position, User

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'alias')

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name', 'alias')


class UserGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'is_active', 'position', 'department')
        read_only_fields = ('username', 'first_name')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'password', 'department', 'position')
        write_only_fields = ('password', )
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', 'date_joined', 'last_login', 
                'first_name', 'image', 'address', 'skill', 'phone_number', 'self_introduction', 'email', 'layout_config', 
                'department', 'position')
        read_only_fields = ('username', 'is_active', 'date_joined', 'last_login', 'department', 'position')
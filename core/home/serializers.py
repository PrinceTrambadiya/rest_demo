from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User

class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username is taken')
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Username is taken')
        
        return data
            
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ColorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class PeopleSerializers(serializers.ModelSerializer):
    color = ColorSerializers()
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        # fields = ['name', 'age']
        fields = '__all__'
        # depth = 1

    # def validate_age(self, data):
    #     print(data)
    #     return data

    # def validate_name(self, data):
    #     print(data)
    #     return data

    def get_color_info(self, obj):
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color_name' : color_obj.color_name, 'hex_code' : '#00000'}

    def validate(self, data):
        special_characters = "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('SC is not allowed')

        if data['age'] < 18:
            raise serializers.ValidationError('age should grate then 18')
        
        return data
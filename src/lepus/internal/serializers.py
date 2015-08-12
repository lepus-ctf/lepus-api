# encoding=utf-8

from rest_framework import serializers

from lepus.models import *

class AttacpPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackPoint
        fields = ('id', 'user', 'team', 'question', 'point', 'token', 'created_at', 'updated_at')
        read_only_fields = ('id', 'team', 'created_at', 'updated_at')

    def validate(self, validated_data):
        user = validated_data.get("user")
        if user:
            validated_data["team"] = user.team
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "ip")

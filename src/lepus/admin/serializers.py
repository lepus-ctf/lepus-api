# encoding=utf-8

from rest_framework import serializers

from lepus.models import *
from lepus.serializers import TeamSerializer, CategorySerializer

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "team", "seat", "points", "ip", "last_score_time", "created_at", "updated_at")
        read_only_fields = ("id", "points", "last_score_time", "ip", "created_at", "updated_at")
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = super(AdminUserSerializer, self).create(validated_data)
        if password:
            instance.set_password(validated_data["password"])
        else:
            instance.password = "!"
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super(AdminUserSerializer, self).update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class AdminTeamSerilaizer(TeamSerializer):
    pass

class AdminCategorySerializer(CategorySerializer):
    pass

class AdminQuestionSerializer(serializers.ModelSerializer):
    """問題"""
    class Meta:
        model = Question
        fields = ('id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'max_failure', 'is_public', 'created_at', 'updated_at')
        read_only_fields = ('id', 'points', 'created_at', 'updated_at')

class AdminFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ("id", "question", "flag", "point", "teams", "created_at", "updated_at")
        read_only_fields = ("id", "teams", "created_at", "updated_at")

class AdminAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "user", "team", "question", "answer", "flag", "is_correct", "created_at", "updated_at")
        read_only_fields = ("is_correct",)

class AdminNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'body', 'is_public', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

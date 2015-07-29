# encoding=utf-8

from lepus import models

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ordering', 'updated_at')
        read_only_fields = ('id', 'name', 'ordering', 'updated_at')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = (
            'id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'max_failure', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'max_failure', 'created_at', 'updated_at')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('id', 'url', 'name', 'question', 'created_at', 'updated_at')
        read_only_fields = ('id', 'url', 'name', 'question', 'created_at', 'updated_at')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id', 'name', 'display_name', 'token', 'last_score_time', 'created_at')
        read_only_fields = ('id', 'name', 'token', 'last_score_time', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'is_staff', 'password', 'last_login', 'last_score_time', 'team', 'seat', 'points')
        read_only_fields = ('id', 'username', 'is_staff', 'last_login', 'last_score_time', 'team', 'seat', 'points')
        extra_kwargs = {'password': {'write_only': True}}

    # TODO:RESTでユーザ作成対応したら頑張る
    # def create(self, validated_data):
    #     try:
    #         team = models.Team.objects.get(name=validated_data['team'])
    #     except models.Team.DoesNotExist:
    #
    #     user = models.User(
    #         username=validated_data['username'],
    #     )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'user', 'team', 'question', 'answer', 'is_correct', 'created_at')
        read_only_fields = ('id', 'user', 'team', 'is_correct', 'created_at')
        extra_kwargs = {'answer': {'write_only': True}}


class AttackPointSerialier(serializers.ModelSerializer):
    class Meta:
        model = models.AttackPoint
        fields = ('id', 'user', 'team', 'question', 'taken', 'point')
        read_only_fields = ('id', 'user', 'team', 'created_at', 'updated_at')


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notice
        fields = ('id', 'title', 'body', 'created_at', 'updated_at')
        read_only_fields = ('id', 'title', 'body', 'created_at', 'updated_at')


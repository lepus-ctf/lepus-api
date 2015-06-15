# encoding=utf-8

from lapus import models

from rest_framework import serializers, status
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ordering', 'created_at', 'updated_at')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'max_failure', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class AdminFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flag
        fields = ('id', 'flag', 'question', 'point', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('id', 'question', 'name', 'file', 'is_public', 'url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'url','created_at', 'updated_at')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id', 'name', 'display_name',  'token', 'last_score_time', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'token', 'id')

# encoding=utf-8

from lapus import models

from rest_framework import serializers, status
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ordering', 'created_at', 'updated_at')

class QuestionSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all())
    
    class Meta:
        model = models.Question
        fields = ('id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'max_failure', 'is_public', 'created_at', 'updated_at')
        extra_kwargs = {'is_public' : {'write_only' : True}}

class FlagSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=models.Question.objects.all())
    
    class Meta:
        model = models.Flag
        fields = ('id', 'flag', 'question', 'point', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class FileSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=models.Question.objects.all())
    
    class Meta:
        model = models.File
        fields = ('id', 'question', 'name', 'file', 'is_public', 'url', 'created_at', 'updated_at')
        read_only_fields = ('url','created_at', 'updated_at')
        extra_kwargs = {'is_public' : {'write_only' : True}}

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id', 'name', 'display_name', 'password', 'token', 'last_score_time', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'token', 'id')
        extra_kwargs = {'password' : {'write_only' : True}}
    
    def create(self, validated_data):
        team = models.Team(
                name = validated_data['name'],
                display_name = validated_data['display_name']
                )
        team.set_password(validated_data['password'])
        team.save()
        return team

    def update(self, validated_data):
        

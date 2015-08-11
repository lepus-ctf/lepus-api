# encoding=utf-8
from django.contrib.auth import authenticate

from datetime import datetime

from lepus import models, validators

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


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, allow_null=False,
                                     error_messages={"require": "ユーザネームは必須です"})  # "ユーザネーム"
    password = serializers.CharField(allow_null=False, error_messages={"require": "パスワードは必須です"})  # "パスワード"

    def __init__(self, data):
        self.username = data.get("username")
        self.password = data.get("password")

        super(AuthSerializer, self).__init__()

    def validate(self, data):
        if not authenticate(username=data['username'], password=data['password']):
            return validators.AuthenticationError('ユーザ名もしくはパスワードが間違っています')
        return data

    def get_authenticate_user(self):
        user = authenticate(username=self.username, password=self.password)

        if not user:
            return False

        return user


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('question', 'answer', 'is_correct')
        read_only_fields = ('is_correct',)
        extra_kwargs = {'answer': {'write_only': True}}

    def validate(self, data):
        question = data['question']
        team = self.context.get('request').user.team

        # 対応するFlagの取得
        try:
            flag = models.Flag.objects.get(question=question, flag=data['answer'])
        except models.Flag.DoesNotExist:
            flag = None

        # 重複を許さない
        if flag and models.Answer.objects.filter(team=team, flag=flag).exists():
            raise serializers.ValidationError("既に解答済みです")

        # questionにおいて制限数が1以上の時，無制限に解答を受け付ける
        if question.max_failure > 0:
            if question.max_failure <= models.Answer.objects.filter(question=question, team=team).count():
                raise serializers.ValidationError("解答制限数を超えました")

        if question.max_answers > 0:
            if question.max_answers <= models.Answer.objects.filter(flag=flag, question=question).count():
                raise serializers.ValidationError("最大正答者数を超えました")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        validated_data['team'] = validated_data['user'].team

        try:
            validated_data['flag'] = models.Flag.objects.get(question=validated_data['question'],
                                                             flag=validated_data['answer'])
        except models.Flag.DoesNotExist:
            pass

        # 正解時に最終得点日時を更新する
        if 'flag' in validated_data:
            validated_data['team'].last_score_time = datetime.now()
            validated_data['team'].save()

        return super(AnswerSerializer, self).create(validated_data)


class AttackPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttackPoint
        fields = ('id', 'user', 'team', 'question', 'taken', 'point')
        read_only_fields = ('id', 'user', 'team', 'created_at', 'updated_at')


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notice
        fields = ('id', 'title', 'body', 'created_at', 'updated_at')
        read_only_fields = ('id', 'title', 'body', 'created_at', 'updated_at')

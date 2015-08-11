# encoding=utf-8
from django.contrib.auth import authenticate

from datetime import datetime

from lepus import models

from rest_framework import serializers, status, exceptions


class AuthenticationError(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリ"""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ordering', 'updated_at')


class QuestionSerializer(serializers.ModelSerializer):
    """問題"""
    class Meta:
        model = models.Question
        fields = (
            'id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'max_failure', 'created_at', 'updated_at')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ('id', 'url', 'name', 'question', 'created_at', 'updated_at')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id', 'name', 'display_name', 'token', 'last_score_time', 'created_at')


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
    username = serializers.CharField(max_length=30, allow_null=False, error_messages={"require":"ユーザネームは必須です"}) # "ユーザネーム"
    password = serializers.CharField(allow_null=False, error_messages={"require":"パスワードは必須です"}) #"パスワード"

    def validate(self, data):
        self._user_cache = None
        if data.get("username") and data.get("password"):
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                self._user_cache = user

        if not self._user_cache:
            raise AuthenticationError('ユーザ名もしくはパスワードが間違っています')
        return data

    def get_user(self):
        return self._user_cache


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('question', 'answer', 'is_correct')
        read_only_fields = ('is_correct',)

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
        if question.max_failure and question.max_failure >= 0:
            if question.max_failure <= models.Answer.objects.filter(question=question, team=team).count():
                raise serializers.ValidationError("解答制限数を超えました")

        if question.max_answers and question.max_answers >= 0:
            if question.max_answers <= models.Answer.objects.filter(flag=flag, question=question).count():
                raise serializers.ValidationError("最大正答者数を超えました")

        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        team = user.team

        question = validated_data['question']
        answer = validated_data['answer']
        flag = None
        try:
            flag = models.Flag.objects.get(question=question, flag=answer)
        except models.Flag.DoesNotExist:
            pass

        # 正解時に最終得点日時を更新する
        if flag:
            team.last_score_time = datetime.now()
            user.last_score_time = datetime.now()
            team.save()
            user.save()

        data = {
            "user":user,
            "team":team,
            "question":question,
            "answer":answer,
            "flag":flag
        }
        answer = models.Answer(**data)
        answer.save()
        return answer


class AttackPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttackPoint
        fields = ('id', 'user', 'team', 'question', 'taken', 'point')
        read_only_fields = ('id', 'user', 'team', 'created_at', 'updated_at')


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notice
        fields = ('id', 'title', 'body', 'created_at', 'updated_at')

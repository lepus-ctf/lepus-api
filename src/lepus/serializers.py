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
        fields = ('question', 'answer', 'is_correct')
        read_only_fields = ('is_correct',)
        extra_kwargs = {'answer': {'write_only': True}}

    def validate(self, attrs):
        question = attrs['question']
        user = self.context.get('request').user

        # 対応するFlagの取得
        try:
            flag = models.Flag.objects.filter(flag=attrs['answer'])
        except models.Flag.DoesNotExist:
            flag = None

        # 重複を許さない
        if flag and models.Answer.objects.filter(user=user, flag=flag):
            raise serializers.ValidationError("既に解答済みです")

        # questionにおいて制限数が0以下の時，無制限に解答を受け付ける
        if question.max_failure > 0 or question.max_answers > 0:
            if question.max_answers <= models.Answer.objects.filter(flag=flag, question=question).count():
                raise serializers.ValidationError("最大正答者数を超えました")
            if question.max_failure >= models.Answer.objects.filter(question=question, user=user).count():
                raise serializers.ValidationError("解答制限数を超えました")

        return attrs

    def create(self, validated_data):
        answer = models.Answer(**validated_data)
        user = self.context.get('request').user
        answer.user = user
        answer.team = user.team

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
        read_only_fields = ('id', 'title', 'body', 'created_at', 'updated_at')

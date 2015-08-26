# encoding=utf-8
from django.contrib.auth import authenticate
from django.conf import settings

from datetime import datetime

from lepus import models

from rest_framework import serializers, status, exceptions, fields


class ValidationErrorDetail(object):
    def __init__(self, error="", message=""):
        self.error = error
        self.message = message


class ValidationError(serializers.ValidationError):

    def __init__(self, error="", message=""):
        detail = ValidationErrorDetail(message=message, error=error)
        super(ValidationError, self).__init__(detail)


class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(BaseSerializer, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if field.read_only:
                continue
            field.error_messages.update({
                "required":"required",
                "null":"required",
                "blank":"required",
                "max_length":"too_long",
                "min_length":"too_short",
                "min_value":"too_small",
                "max_value":"too_big",
                "invalid":"invalid",
                "max_string_length":"too_long",
                "does_not_exist":"not_found",
                "incorrect_type":"numeric_is_required"
            })

            if isinstance(field, fields.IntegerField):
                field.error_messages.update({
                    "invalid":"numeric_is_required"
                })


class CategorySerializer(BaseSerializer):
    """カテゴリ"""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ordering', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class FileSerializer(BaseSerializer):
    class Meta:
        model = models.File
        fields = ('url', 'name', 'created_at', 'updated_at')


class QuestionSerializer(BaseSerializer):
    """問題"""

    class Meta:
        model = models.Question
        fields = (
            'id', 'category', 'ordering', 'title', 'sentence', 'max_answers', 'files', 'max_failure',
            'created_at', 'updated_at', 'points'
        )
        read_only_fields = ('points', )

    files = FileSerializer(many=True, read_only=True)


class TeamSerializer(BaseSerializer):
    class Meta:
        model = models.Team
        fields = (
            'id', 'name', 'password', 'token', 'points', 'last_score_time', 'created_at', 'updated_at',
            'questions')
        read_only_fields = ('id', 'token', 'points', 'last_score_time', 'questions', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = super(TeamSerializer, self).create(validated_data)
        if password:
            instance.set_password(validated_data["password"])
        else:
            instance.password = "!"
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super(TeamSerializer, self).update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class UserSerializer(BaseSerializer):
    class Meta:
        model = models.User
        fields = ("id", "username", "password", "team", "points", "last_score_time", "team_name", "team_password", "is_staff")
        read_only_fields = ("id", "team", "points", "last_score_time", "is_staff")
        extra_kwargs = {'password': {'write_only': True}}

    team_name = serializers.CharField(write_only=True, allow_null=False)
    team_password = serializers.CharField(write_only=True, allow_null=False)

    def validate_password(self, value):
        # FIXME:許可するパターンを指定
        return value

    def validate(self, data):
        team = None
        try:
            team = models.Team.objects.get(name=data.get("team_name"))
            if not team.check_password(data.get("team_password")):
                raise models.Team.DoesNotExist()
        except models.Team.DoesNotExist:
            if team or not settings.ALLOW_CREATE_USER:
                # パスワード間違い，または，登録が禁止されている場合
                raise ValidationError(message="Invalid credentials. Team name or password is invalid.", error="INVALID_CREDENTIALS")

        data["team"] = team
        return data

    def create(self, validated_data):
        team = validated_data["team"]
        if not team:
            # チームの作成
            team = models.Team(name=validated_data["team_name"])
            team.set_password(validated_data["team_password"])
            team.save()

        # ユーザーの作成とパスワードの設定
        user_data = {
            "team": team,
            "username": validated_data["username"]
        }
        user = models.User(**user_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, allow_null=False, error_messages={"required":"required"})
    password = serializers.CharField(allow_null=False, error_messages={"required":"required"})

    def validate(self, data):
        self._user_cache = None
        if data.get("username") and data.get("password"):
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                self._user_cache = user

        if not self._user_cache:
            raise ValidationError(message="Authentication failure. Username or password is invalid.", error="INVALID_CREDENTIALS")
        return data

    def get_user(self):
        return self._user_cache


class AnswerSerializer(BaseSerializer):
    class Meta:
        model = models.Answer
        fields = ('question', 'answer', 'is_correct')
        read_only_fields = ('is_correct',)

    def validate(self, data):
        question = data['question']
        user = self.context.get('request').user
        team = user.team

        # 対応するFlagの取得
        try:
            flag = models.Flag.objects.get(question=question, flag=data['answer'])
        except models.Flag.DoesNotExist:
            # 間違いを記録
            answer = models.Answer(question=question, team=team, user=user, answer=data['answer'], flag=None)
            answer.save()
            raise ValidationError(message="This answer is not correct.", error="INCORRECT_ANSWER")

        # 重複を許さない
        if flag and models.Answer.objects.filter(team=team, flag=flag).exists():
            raise ValidationError(message="The flag is already submitted.", error="ALREADY_SUBMITTED")

        # questionにおいて制限数が1以上の時，無制限に解答を受け付ける
        if question.max_failure and question.max_failure >= 0:
            if question.max_failure <= models.Answer.objects.filter(question=question, team=team).count():
                raise ValidationError(message="Failure count is exceed. You can't submit for this question.", error="MAX_FAILURE")

        if question.max_answers and question.max_answers >= 0:
            if question.max_answers <= models.Answer.objects.filter(flag=flag, question=question).count():
                raise ValidationError(message="Teams count is exceed. You can't submit for this question.", error="MAX_ANSWERS")

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
            "user": user,
            "team": team,
            "question": question,
            "answer": answer,
            "flag": flag
        }
        answer = models.Answer(**data)
        answer.save()
        return answer


class AttackPointSerializer(BaseSerializer):
    class Meta:
        model = models.AttackPoint
        fields = ('id', 'user', 'team', 'question', 'taken', 'point')
        read_only_fields = ('id', 'user', 'team', 'created_at', 'updated_at')


class NoticeSerializer(BaseSerializer):
    class Meta:
        model = models.Notice
        fields = ('id', 'title', 'body', 'created_at', 'updated_at')


class ConfigSerializer(BaseSerializer):
    class Meta:
        model = models.Config
        fields = ('id', 'value')
        readonly_fields = ('id', 'value')

    id = serializers.CharField(source='key')

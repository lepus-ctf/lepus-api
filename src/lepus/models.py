# encoding=utf-8
import pickle
import hashlib
import time
import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

class Templete(models.Model):
    """全てのモデルで共通のフィールドを含んだAbstract Model"""
    class Meta:
        abstract = True
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

class Category(Templete):
    """問題のカテゴリ"""
    class Meta:
        ordering = ['ordering']
        unique_together = (('name', 'ordering'),)
    name = models.CharField("カテゴリ名", max_length=50)
    ordering = models.IntegerField("表示順序", default=100)

    def __str__(self):
        return self.name

class Question(Templete):
    """問題"""
    class Meta:
        ordering = ['ordering']
    category = models.ForeignKey(Category, verbose_name="カテゴリ")
    ordering = models.IntegerField("表示順序", default=100, unique=True)
    title = models.CharField("タイトル", max_length=50)
    sentence = models.TextField("問題文")
    max_answers = models.IntegerField("最大回答者数", blank=True, null=True)
    max_failure = models.IntegerField("最大回答数", blank=True, null=True)
    is_public = models.BooleanField("公開にするか", blank=True, default=False)

    def __str__(self):
        return self.title

class Flag(Templete):
    """正解のフラグと得点"""
    flag = models.CharField("Flag", max_length=200, unique=True)
    question = models.ForeignKey(Question, verbose_name="問題")
    point = models.IntegerField("得点")

    def __str__(self):
        return self.flag

class File(Templete):
    """問題に添付するファイル"""
    question = models.ForeignKey(Question, verbose_name="問題")
    name = models.CharField("ファイル名", max_length=256)
    file = models.FileField(upload_to='question/', max_length=256, verbose_name="ファイル")
    is_public = models.BooleanField("公開するか", blank=True, default=True)

    @property
    def url(self):
        return reverse('score.views.file_download', args=[self.id])

    def __str__(self):
        return self.name

class Team(Templete):
    """チーム"""
    name = models.CharField("チーム名", max_length=32, unique=True)
    display_name = models.CharField("表示名", max_length=32, unique=True)
    password = models.CharField("チームパスワード", max_length=128)
    last_score_time = models.DateTimeField("最終得点日時", blank=True, null=True)

    def __str__(self):
        return self.name

    def set_password(self, password):
        self.password = make_password(password)


    @property
    def token(self):
        sha1 = hashlib.sha1()
        sha1.update("{0}_{1}_{2}".format(
                                         settings.TEAM_TOKEN_SECRET_KEY,
                                         self.id,
                                         int(time.time() / settings.TEAM_TOKEN_INTERVAL
                                             )).encode("utf-8"))
        return sha1.hexdigest()

    @property
    def points(self):
        answers = Answer.objects.filter(team=self).exclude(flag=None)
        points = 0
        for answer in answers:
            points += answer.flag.point

        return points


class User(AbstractUser, Templete):
    """チームに属するユーザ"""
    team = models.ForeignKey(Team, verbose_name="チーム", blank=True, null=True)
    seat = models.CharField("座席", max_length=32, blank=True)
    last_score_time = models.DateTimeField("最終得点日時", blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def points(self):
        answers = Answer.objects.filter(user=self).exclude(flag=None)
        points = 0
        for answer in answers:
            points += answer.flag.point

        return points

class UserConnection(Templete):
    """ユーザの接続元を管理するモデル"""
    class Meta:
        unique_together = (('user', 'ip'),)
        ordering = ("-updated_at",)

    user = models.ForeignKey(User, verbose_name="ユーザー")
    ip = models.GenericIPAddressField("IPアドレス")

    @classmethod
    def update(cls, user, ip):
        """アクセス元IPの更新"""
        user_connection, created = cls.objects.get_or_create(user=user, ip=ip)
        if not created:
            user_connection.updated_at = datetime.datetime.now()
            user_connection.save()
        return user_connection

class Answer(Templete):
    """回答履歴"""
    class Meta:
        unique_together = (('team', 'flag'),)
    user = models.ForeignKey(User, verbose_name="ユーザー")
    team = models.ForeignKey(Team, verbose_name="チーム")
    question = models.ForeignKey(Question, verbose_name="問題")
    flag = models.ForeignKey(Flag, blank=True, null=True)
    answer = models.CharField("解答", max_length=256)

    @property
    def is_correct(self):
        return self.flag is not None

class AttackPoint(Templete):
    """攻撃点記録"""
    user = models.ForeignKey(User, verbose_name="ユーザー")
    team = models.ForeignKey(Team, verbose_name="チーム")
    question = models.ForeignKey(Question, verbose_name="問題")
    token = models.CharField("トークン", max_length=256, unique=True)
    point = models.IntegerField("得点")

class Config(Templete):
    """設定用モデル"""
    key = models.CharField("設定項目", max_length=256, unique=True)
    value_str = models.TextField("シリアライズされた値")

    def __str__(self):
        return self.key

    def get_value(self):
        return pickle.loads(self.value_str)
    def set_value(self, value):
        self.value_str = pickle.dumps(value)
    value = property(get_value, set_value)

class Notice(Templete):
    """お知らせ"""
    class Meta:
        ordering = ['created_at']
    title = models.CharField("タイトル", max_length=80)
    body = models.TextField("本文")

    def __str__(self):
        return self.title

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import lepus.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, max_length=30)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('seat', models.CharField(blank=True, verbose_name='座席', max_length=32)),
                ('last_score_time', models.DateTimeField(blank=True, verbose_name='最終得点日時', null=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='user_set', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', lepus.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('answer', models.CharField(verbose_name='解答', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='AttackPoint',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('token', models.CharField(unique=True, verbose_name='トークン', max_length=256)),
                ('point', models.IntegerField(verbose_name='得点')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('name', models.CharField(verbose_name='カテゴリ名', max_length=50)),
                ('ordering', models.IntegerField(verbose_name='表示順序', default=100)),
            ],
            options={
                'ordering': ('ordering',),
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('key', models.CharField(unique=True, verbose_name='設定項目', max_length=256)),
                ('value_str', models.TextField(verbose_name='シリアライズされた値')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('name', models.CharField(verbose_name='ファイル名', max_length=256)),
                ('file', models.FileField(upload_to='question/', verbose_name='ファイル', max_length=256)),
                ('is_public', models.BooleanField(verbose_name='公開するか', default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('flag', models.CharField(unique=True, verbose_name='Flag', max_length=200)),
                ('point', models.IntegerField(verbose_name='得点')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('title', models.CharField(verbose_name='タイトル', max_length=80)),
                ('body', models.TextField(verbose_name='本文')),
                ('is_public', models.BooleanField(verbose_name='公開にするか', default=False)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('ordering', models.IntegerField(unique=True, verbose_name='表示順序', default=100)),
                ('title', models.CharField(verbose_name='タイトル', max_length=50)),
                ('sentence', models.TextField(verbose_name='問題文')),
                ('max_answers', models.IntegerField(blank=True, verbose_name='最大回答者数', null=True)),
                ('max_failure', models.IntegerField(blank=True, verbose_name='最大回答数', null=True)),
                ('is_public', models.BooleanField(verbose_name='公開にするか', default=False)),
                ('category', models.ForeignKey(to='lepus.Category', verbose_name='カテゴリ')),
            ],
            options={
                'ordering': ('ordering',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('name', models.CharField(unique=True, verbose_name='チーム名', max_length=32)),
                ('password', models.CharField(verbose_name='チームパスワード', max_length=128)),
                ('last_score_time', models.DateTimeField(blank=True, verbose_name='最終得点日時', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserConnection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='作成日時', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='最終更新日時', auto_now=True)),
                ('ip', models.GenericIPAddressField(verbose_name='IPアドレス')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
        migrations.AddField(
            model_name='flag',
            name='question',
            field=models.ForeignKey(to='lepus.Question', verbose_name='問題'),
        ),
        migrations.AddField(
            model_name='file',
            name='question',
            field=models.ForeignKey(to='lepus.Question', verbose_name='問題'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name', 'ordering')]),
        ),
        migrations.AddField(
            model_name='attackpoint',
            name='question',
            field=models.ForeignKey(to='lepus.Question', verbose_name='問題'),
        ),
        migrations.AddField(
            model_name='attackpoint',
            name='team',
            field=models.ForeignKey(to='lepus.Team', verbose_name='チーム'),
        ),
        migrations.AddField(
            model_name='attackpoint',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AddField(
            model_name='answer',
            name='flag',
            field=models.ForeignKey(to='lepus.Flag', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='lepus.Question', verbose_name='問題'),
        ),
        migrations.AddField(
            model_name='answer',
            name='team',
            field=models.ForeignKey(to='lepus.Team', verbose_name='チーム'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(to='lepus.Team', blank=True, verbose_name='チーム', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', related_name='user_set', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_query_name='user'),
        ),
        migrations.AlterUniqueTogether(
            name='userconnection',
            unique_together=set([('user', 'ip')]),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('team', 'flag')]),
        ),
    ]

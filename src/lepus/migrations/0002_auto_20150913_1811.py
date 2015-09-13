# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lepus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('ordering', 'id')},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('category__ordering', 'ordering', 'id')},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='カテゴリ名', unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='ordering',
            field=models.IntegerField(verbose_name='表示順序', default=100),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([]),
        ),
    ]

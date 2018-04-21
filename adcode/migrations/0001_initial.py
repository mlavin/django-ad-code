# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adcode.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('remote_id', models.CharField(default='', max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('pattern', models.CharField(max_length=200, validators=[adcode.validators.validate_pattern])),
                ('priority', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('width', models.PositiveSmallIntegerField()),
                ('height', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='placement',
            name='sections',
            field=models.ManyToManyField(related_name='placements', to='adcode.Section', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='placement',
            name='size',
            field=models.ForeignKey(related_name='placements', to='adcode.Size', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]

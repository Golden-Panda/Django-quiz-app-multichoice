# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000)),
                ('correct', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Ответы',
                'verbose_name': 'Ответ',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('figure', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d')),
                ('content', models.CharField(max_length=1000)),
                ('random_order', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Вопросы',
                'verbose_name': 'Вопрос',
                'ordering': ['subject'],
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('url', models.SlugField(max_length=120)),
                ('random_order', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Тесты',
                'verbose_name': 'Тест',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Предметы',
                'verbose_name': 'Предмет',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voud_quiz.Subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(blank=True, to='voud_quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='voud_quiz.Subject'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voud_quiz.Question'),
        ),
    ]

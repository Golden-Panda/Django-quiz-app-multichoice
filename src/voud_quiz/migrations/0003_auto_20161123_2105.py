# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voud_quiz', '0002_auto_20161122_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voud_quiz.Question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(blank=True, to='voud_quiz.Quiz', verbose_name='Тест'),
        ),
    ]

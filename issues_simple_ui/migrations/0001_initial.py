# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-03 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, help_text='an identifier used by the system to place this content', max_length=64, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContentTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('content', models.TextField(blank=True)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='issues_simple_ui.Content')),
            ],
            options={
                'verbose_name': 'content Translation',
                'managed': True,
                'db_table': 'issues_simple_ui_content_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, help_text='an identifier used by the system to place this image', max_length=64, unique=True)),
                ('file', models.FileField(upload_to='ui/img')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contenttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]

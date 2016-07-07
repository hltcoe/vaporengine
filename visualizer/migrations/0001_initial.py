# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zr_fragment_index', models.IntegerField()),
                ('start_offset', models.IntegerField()),
                ('end_offset', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('audio_rate', models.IntegerField()),
                ('audio_channels', models.IntegerField()),
                ('audio_precision', models.IntegerField()),
                ('protected_corpus', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_index', models.IntegerField()),
                ('audio_path', models.TextField()),
                ('audio_identifier', models.TextField()),
                ('duration', models.IntegerField()),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Corpus')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField()),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Corpus')),
                ('documents', models.ManyToManyField(to='visualizer.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField()),
                ('zr_term_index', models.IntegerField()),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='audiofragment',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Document'),
        ),
        migrations.AddField(
            model_name='audiofragment',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.Term'),
        ),
    ]

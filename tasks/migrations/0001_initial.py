# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import tasks.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom_result', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('selected_geocoder', models.SmallIntegerField(default=0)),
                ('coord_Google', models.CharField(max_length=100, null=True)),
                ('coord_Bing', models.CharField(max_length=100, null=True)),
                ('coord_Here', models.CharField(max_length=100, null=True)),
                ('coord_OSM', models.CharField(max_length=100, null=True)),
                ('quality_Google', models.CharField(max_length=100, null=True)),
                ('quality_Bing', models.CharField(max_length=100, null=True)),
                ('quality_Here', models.CharField(max_length=100, null=True)),
                ('quality_OSM', models.CharField(max_length=100, null=True)),
                ('accuracy_Google', models.CharField(max_length=100, null=True)),
                ('accuracy_Bing', models.CharField(max_length=100, null=True)),
                ('accuracy_Here', models.CharField(max_length=100, null=True)),
                ('accuracy_OSM', models.CharField(max_length=100, null=True)),
                ('confidence_Google', models.CharField(max_length=100, null=True)),
                ('confidence_Bing', models.CharField(max_length=100, null=True)),
                ('confidence_Here', models.CharField(max_length=100, null=True)),
                ('confidence_OSM', models.CharField(max_length=100, null=True)),
                ('suggested_Coord', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('max_number_answers', models.SmallIntegerField(help_text=b'Please enter the number of task answers needed for an address to be considered completed.')),
                ('null_number_answers', models.SmallIntegerField(help_text=b'Please enter the number of null task answers to consider an address invalid.')),
                ('reward_is_offered', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'SB', max_length=2, choices=[(b'SB', b'Standby'), (b'IP', b'In process'), (b'F', b'Completed')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_text', models.CharField(default=b'', max_length=200)),
                ('status', models.CharField(default=b'IP', max_length=2, choices=[(b'IP', b'In process'), (b'F', b'Completed')])),
                ('task_name', models.ForeignKey(to='tasks.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAddressFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_file', models.FileField(help_text=b'Upload a CSV file (UTF-8 encoded) with addresses text data at first column starting at second row. First row is considered as the field title header and is going to be ignored', upload_to=tasks.models.upload_to)),
                ('task', models.ForeignKey(help_text=b'Make sure to select one task!', to='tasks.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskReward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('reward_goal', models.SmallIntegerField(default=100, help_text=b'Please enter the number of task addresses to be done by a user to obtain the reward.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=b'Update this to know more about you!', null=True)),
                ('my_postal_code', models.CharField(max_length=120, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('my_rewards', models.ManyToManyField(to='tasks.TaskReward', blank=True)),
                ('my_tasks', models.ManyToManyField(help_text=b'Tasks where I am participating.', related_name='my_tasks', to='tasks.Task', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='addressresult',
            name='address',
            field=models.ForeignKey(to='tasks.TaskAddress'),
        ),
        migrations.AddField(
            model_name='addressresult',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='addressresult',
            unique_together=set([('user', 'address')]),
        ),
    ]

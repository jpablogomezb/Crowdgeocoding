# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='my_rewards',
            field=models.ManyToManyField(related_name='my_rewards', to='tasks.TaskReward', blank=True),
        ),
    ]

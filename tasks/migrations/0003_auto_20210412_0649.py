# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210405_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addressresult',
            old_name='accuracy_Here',
            new_name='accuracy_Mapquest',
        ),
        migrations.RenameField(
            model_name='addressresult',
            old_name='confidence_Here',
            new_name='confidence_Mapquest',
        ),
        migrations.RenameField(
            model_name='addressresult',
            old_name='coord_Here',
            new_name='coord_Mapquest',
        ),
        migrations.RenameField(
            model_name='addressresult',
            old_name='quality_Here',
            new_name='quality_Mapquest',
        ),
    ]

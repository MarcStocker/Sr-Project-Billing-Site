# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20170323_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitybill',
            name='house',
            field=models.ForeignKey(db_constraint=False, default='1', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.Lease'),
        ),
    ]

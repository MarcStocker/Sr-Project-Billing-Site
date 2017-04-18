# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommate',
            name='ioutotaldebt',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='ioutotalowed',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='ioutotalpaid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='ioutotalremaining',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='utilpercentowed',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='utiltotaldebt',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='utiltotalowed',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='utiltotalpaid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='roommate',
            name='utiltotalremaining',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
    ]

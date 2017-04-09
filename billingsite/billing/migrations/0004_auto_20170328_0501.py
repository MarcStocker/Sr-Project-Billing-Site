# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 05:01
from __future__ import unicode_literals

import billing.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_auto_20170320_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilitybill',
            name='image',
        ),
        migrations.AddField(
            model_name='utilitybill',
            name='billdoc',
            field=models.FileField(blank=True, default=' ', max_length=144, null=True, upload_to=billing.models.bill_directory_path),
        ),
        migrations.AlterField(
            model_name='utilitybill',
            name='datepaid',
            field=models.DateField(blank=True, default='', null=True),
        ),
    ]
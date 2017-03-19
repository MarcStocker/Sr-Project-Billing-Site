# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 21:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='billPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payType', models.TextField()),
            ],
            options={
                'ordering': ('id', 'date'),
            },
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
            options={
                'ordering': ('id', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Roommate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('house', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.Lease')),
                ('user', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id', 'name'),
            },
        ),
        migrations.CreateModel(
            name='userPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payType', models.TextField()),
                ('payee', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='payee', to='billing.Roommate')),
                ('payer', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='payer', to='billing.Roommate')),
            ],
            options={
                'ordering': ('id', 'date'),
            },
        ),
        migrations.CreateModel(
            name='UtilityBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dueDate', models.DateField(blank=True, null=True)),
                ('statementDate', models.DateField(blank=True, null=True)),
                ('datepaid', models.DateField(blank=True, null=True)),
                ('image', models.FileField(blank=True, default='', max_length=144, null=True, upload_to='uploads/%Y/%m%d/')),
                ('house', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.Lease')),
                ('owner', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.Roommate')),
            ],
            options={
                'ordering': ('id', 'dueDate'),
            },
        ),
        migrations.CreateModel(
            name='UtilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('website', models.CharField(max_length=200)),
                ('serviceType', models.CharField(max_length=50)),
                ('image', models.FileField(blank=True, max_length=144, null=True, upload_to='uploads/%Y/%m/%d/')),
            ],
            options={
                'ordering': ('id', 'name'),
            },
        ),
        migrations.AddField(
            model_name='utilitybill',
            name='utilType',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.UtilityType'),
        ),
        migrations.AddField(
            model_name='billpayment',
            name='UtilBill',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.UtilityBill'),
        ),
        migrations.AddField(
            model_name='billpayment',
            name='payer',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='billing.Roommate'),
        ),
    ]

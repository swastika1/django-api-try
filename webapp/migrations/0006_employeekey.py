# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-05 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20190605_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_key', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employeekeys', to='webapp.Employee')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]

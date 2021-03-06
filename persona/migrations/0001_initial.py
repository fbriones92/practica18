# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruc', models.CharField(max_length=13)),
                ('nombre_comercial', models.CharField(max_length=200)),
                ('observaciones', models.TextField(blank=True, max_length=2000, null=True)),
                ('actividad_economica', models.TextField(null=True)),
                ('producto_servicio', models.TextField(null=True)),
                ('tipo', models.SmallIntegerField()),
            ],
        ),
    ]

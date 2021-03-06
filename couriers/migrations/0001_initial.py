# Generated by Django 3.1.7 on 2021-03-21 10:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier_id', models.IntegerField(db_index=True, unique=True, verbose_name='Идентификатор курьера')),
                ('courier_type', models.CharField(choices=[('foot', 10), ('bike', 15), ('car', 50)], max_length=4, verbose_name='Тип курьера')),
                ('regions', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None, verbose_name='Список идентификаторов районов')),
                ('working_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=11), size=None, verbose_name='График работы курьера')),
            ],
        ),
    ]

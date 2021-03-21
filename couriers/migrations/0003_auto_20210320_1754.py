# Generated by Django 3.1.7 on 2021-03-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('couriers', '0002_auto_20210319_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='courier_type',
            field=models.CharField(choices=[('foot', 10), ('bike', 15), ('car', 50)], max_length=4, verbose_name='Тип курьера'),
        ),
    ]
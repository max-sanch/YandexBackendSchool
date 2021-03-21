# Generated by Django 3.1.7 on 2021-03-20 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210320_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='courier_type',
            field=models.CharField(choices=[('foot', 10), ('bike', 15), ('car', 50)], max_length=4, verbose_name='Тип курьера исполняющего заказ'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='end_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='Окончание выполнения заказа'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='start_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='Начало выполнения заказа'),
        ),
    ]
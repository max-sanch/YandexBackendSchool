# Generated by Django 3.1.7 on 2021-03-21 10:33

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('couriers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(db_index=True, unique=True, verbose_name='Идентификатор заказа')),
                ('weight', models.FloatField(verbose_name='Вес заказа')),
                ('region', models.IntegerField(verbose_name='Район доставки заказа')),
                ('delivery_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=11), size=None, verbose_name='Промежутки приёма заказов')),
                ('status', models.IntegerField(choices=[(0, 'Новый'), (1, 'В работе'), (2, 'Завершённый')], default=0, verbose_name='Вес заказа')),
            ],
        ),
        migrations.CreateModel(
            name='OrderGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_time', models.DateTimeField(auto_now_add=True, verbose_name='Время выбора заказов')),
                ('courier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='couriers.courier', verbose_name='Курьер выполняющий группу заказов')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.IntegerField(verbose_name='Район доставки заказа')),
                ('courier_type', models.CharField(choices=[('foot', 10), ('bike', 15), ('car', 50)], max_length=4, verbose_name='Тип курьера исполняющего заказ')),
                ('start_time', models.DateTimeField(default=None, null=True, verbose_name='Начало выполнения заказа')),
                ('end_time', models.DateTimeField(default=None, null=True, verbose_name='Окончание выполнения заказа')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='couriers.courier', verbose_name='Курьер выполняющий заказ')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('order_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.ordergroup', verbose_name='Группа заказа')),
            ],
        ),
    ]

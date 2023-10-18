# Generated by Django 4.2.4 on 2023-10-06 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEaseAdmin', '0014_alter_orderreceived_payment_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderreceived',
            name='customer_cancellation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderreceived',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2023, 10, 6, 16, 19, 11, 970022)),
        ),
    ]

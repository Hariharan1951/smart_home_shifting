# Generated by Django 4.2.4 on 2023-10-09 10:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEaseAdmin', '0022_couponcounttable_alter_orderreceived_pickup_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcodetable',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='couponcounttable',
            name='count_per_user',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderreceived',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2023, 10, 9, 15, 56, 59, 884349)),
        ),
    ]

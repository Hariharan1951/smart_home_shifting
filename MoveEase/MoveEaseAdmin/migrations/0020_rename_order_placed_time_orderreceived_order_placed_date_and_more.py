# Generated by Django 4.2.4 on 2023-10-08 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEaseAdmin', '0019_alter_orderreceived_order_cancel_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderreceived',
            old_name='order_placed_time',
            new_name='order_placed_date',
        ),
        migrations.AlterField(
            model_name='orderreceived',
            name='order_cancel_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='orderreceived',
            name='order_completed_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='orderreceived',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2023, 10, 8, 20, 5, 19, 143049)),
        ),
    ]

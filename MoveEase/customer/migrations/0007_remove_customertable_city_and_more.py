# Generated by Django 4.2.4 on 2023-09-24 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_customertable_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customertable',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='door_no',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='state',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='street',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customertable',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='door_no',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='street',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='vehicle_number',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='vehicle_type',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zip_code',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]

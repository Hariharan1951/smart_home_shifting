# Generated by Django 4.2.4 on 2023-09-24 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_remove_customertable_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='vehicle_type',
            field=models.CharField(choices=[('TATA ACE', 'Tata Ace'), ('TATA 407', 'Tata 407'), ('PICKUP', 'Pickup'), ('DOST', 'Dost'), ('SUPER ACE', 'Super Ace'), ('8FT', '8FT'), ('3 WHEELER', '3 Wheeler'), ('3 WHEELER ELECTRIC', '3 Wheeler Electric')], max_length=128, null=True),
        ),
    ]
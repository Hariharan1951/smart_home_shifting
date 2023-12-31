# Generated by Django 4.2.4 on 2023-10-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEaseAdmin', '0003_rename_item_size_itemstable_item_size_ft_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponCodeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('offer_percent', models.IntegerField()),
                ('min_billing_amount', models.IntegerField()),
                ('max_discount_rate', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderReceived',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.IntegerField(null=True)),
                ('customer_name', models.CharField(max_length=128, null=True)),
                ('ph_no', models.CharField(max_length=128, null=True)),
                ('fromAddress', models.CharField(max_length=128, null=True)),
                ('toAddress', models.CharField(max_length=128, null=True)),
                ('shifting_date', models.DateField()),
                ('kms_range', models.IntegerField(null=True)),
                ('no_of_items', models.IntegerField(null=True)),
                ('SOFA_SINGLE', models.IntegerField(null=True)),
                ('SOFA_DOUBLE', models.IntegerField(null=True)),
                ('SOFA_3_SEATER', models.IntegerField(null=True)),
                ('SOFA_4_SEATER', models.IntegerField(null=True)),
                ('BED_SINGLE', models.IntegerField(null=True)),
                ('BED_DOUBLE', models.IntegerField(null=True)),
                ('COT_FOLDING', models.IntegerField(null=True)),
                ('MATTRESS_SINGLE', models.IntegerField(null=True)),
                ('MATTRESS_DOUBLE', models.IntegerField(null=True)),
                ('DINING_TABLE_CHAIRS', models.IntegerField(null=True)),
                ('OFFICE_CHAIRS', models.IntegerField(null=True)),
                ('PLASTIC_CHAIRS', models.IntegerField(null=True)),
                ('DRESSING_TABLE', models.IntegerField(null=True)),
                ('DINING_TABLE', models.IntegerField(null=True)),
                ('COMPUTER_TABLE', models.IntegerField(null=True)),
                ('TV', models.IntegerField(null=True)),
                ('AC', models.IntegerField(null=True)),
                ('FAN', models.IntegerField(null=True)),
                ('FRIDGE', models.IntegerField(null=True)),
                ('WASHING_MACHINE', models.IntegerField(null=True)),
                ('GAS_STOVE', models.IntegerField(null=True)),
                ('MICROWAVE_OVEN', models.IntegerField(null=True)),
                ('WATER_PURIFIER', models.IntegerField(null=True)),
                ('BIKE', models.IntegerField(null=True)),
                ('SCOOTER', models.IntegerField(null=True)),
                ('BICYCLE', models.IntegerField(null=True)),
                ('total_amount', models.IntegerField(null=True)),
                ('booking_amount', models.IntegerField(null=True)),
                ('selected_vehicles', models.CharField(max_length=1000)),
            ],
        ),
    ]

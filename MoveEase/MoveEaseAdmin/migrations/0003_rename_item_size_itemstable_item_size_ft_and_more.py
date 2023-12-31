# Generated by Django 4.2.4 on 2023-09-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEaseAdmin', '0002_alter_itemstable_item_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemstable',
            old_name='item_size',
            new_name='item_size_ft',
        ),
        migrations.AddField(
            model_name='itemstable',
            name='fragility',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='itemstable',
            name='item_category',
            field=models.CharField(choices=[('FURNITURES', 'Furnitures'), ('APPLIANCES', 'Appliances'), ('VEHICLES', 'Vehicles')], default='APPLIANCES', max_length=128),
        ),
    ]

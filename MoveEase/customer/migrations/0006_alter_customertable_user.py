# Generated by Django 4.2.4 on 2023-09-24 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_customertable_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customertable',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

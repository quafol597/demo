# Generated by Django 3.1.7 on 2021-03-16 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210316_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
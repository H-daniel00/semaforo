# Generated by Django 2.2.4 on 2020-01-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direccion', '0027_auto_20200109_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividades',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
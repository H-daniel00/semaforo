# Generated by Django 2.2.4 on 2019-09-19 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direccion', '0010_auto_20190919_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='direcciones',
            name='see_in_list',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='direcciones',
            name='see_in_select',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.2.4 on 2019-09-17 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('direccion', '0008_auto_20190917_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permisos',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permisos', to=settings.AUTH_USER_MODEL),
        ),
    ]
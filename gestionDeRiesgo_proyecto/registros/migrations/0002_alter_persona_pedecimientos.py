# Generated by Django 4.1 on 2024-06-09 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='pedecimientos',
            field=models.ManyToManyField(default='Ninguno', null=True, to='registros.padecimientos'),
        ),
    ]
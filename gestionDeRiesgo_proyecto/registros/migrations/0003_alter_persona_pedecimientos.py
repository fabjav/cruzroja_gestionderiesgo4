# Generated by Django 4.1 on 2024-06-09 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0002_alter_persona_pedecimientos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='pedecimientos',
            field=models.ManyToManyField(blank=True, default='Ninguno', to='registros.padecimientos'),
        ),
    ]
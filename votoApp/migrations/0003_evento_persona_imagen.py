# Generated by Django 5.1.3 on 2024-11-26 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votoApp', '0002_persona_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id_evento', models.AutoField(primary_key=True, serialize=False)),
                ('activo', models.BooleanField(default=False, null=True)),
            ],
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-23 19:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('idpersona', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('ci', models.CharField(max_length=255, unique=True)),
                ('carrera', models.CharField(max_length=255)),
                ('facultad', models.CharField(max_length=255)),
                ('grupo', models.CharField(max_length=255)),
                ('anno_academico', models.CharField(max_length=255)),
                ('solapin', models.CharField(max_length=255, unique=True)),
                ('provincia', models.CharField(max_length=255)),
                ('municipio', models.CharField(max_length=255)),
                ('activo', models.BooleanField(default=True)),
                ('acceso', models.BooleanField(default=True)),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idusuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('contrasena', models.CharField(max_length=8, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.BinaryField()),
                ('idpersona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='imagen', to='votoApp.persona')),
            ],
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-23 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votoApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='acceso',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='activo',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='anno_academico',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='carrera',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='ci',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='facultad',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='fecha',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='grupo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='municipio',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='provincia',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-05 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_rename_bio_perfil_descripcion_remove_perfil_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='apellido',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='descripcion',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='категории',
            name='Категория1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='категории',
            name='Категория2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='категории',
            name='Категория3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='категории',
            name='Категория4',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='категории',
            name='Категория5',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

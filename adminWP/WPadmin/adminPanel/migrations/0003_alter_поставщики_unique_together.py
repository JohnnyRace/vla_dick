# Generated by Django 4.0.2 on 2022-02-21 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0002_alter_категории_категория1_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='поставщики',
            unique_together=set(),
        ),
    ]

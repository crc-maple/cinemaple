# Generated by Django 2.2 on 2019-06-05 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhandling', '0015_auto_20190603_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tmdbID',
            field=models.CharField(max_length=200),
        ),
    ]

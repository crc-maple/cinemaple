# Generated by Django 2.2 on 2019-04-20 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhandling', '0004_auto_20190420_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='MovieNightEvent',
            field=models.ManyToManyField(blank=True, to='userhandling.MovieNightEvent'),
        ),
    ]

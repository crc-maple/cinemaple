# Generated by Django 2.2 on 2019-08-17 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhandling', '0041_auto_20190720_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_buffer',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]

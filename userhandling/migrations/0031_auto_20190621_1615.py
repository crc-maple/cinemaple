# Generated by Django 2.2 on 2019-06-21 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhandling', '0030_votingparameters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movienightevent',
            name='isactive',
        ),
        migrations.AddField(
            model_name='movienightevent',
            name='isdraft',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 2.2 on 2019-06-30 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userhandling', '0034_auto_20190630_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toping',
            name='movienight',
        ),
        migrations.RemoveField(
            model_name='toping',
            name='user',
        ),
        migrations.CreateModel(
            name='MovienightTopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movienight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userhandling.MovieNightEvent')),
                ('toping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userhandling.Toping')),
            ],
        ),
    ]

# Generated by Django 2.2 on 2019-07-20 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userhandling', '0040_auto_20190720_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattendence',
            name='registration_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movienighttopping',
            name='user_attendence',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='userhandling.UserAttendence'),
        ),
        migrations.AlterField(
            model_name='votepreference',
            name='user_attendence',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='userhandling.UserAttendence'),
        ),
    ]

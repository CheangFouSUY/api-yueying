# Generated by Django 4.0.3 on 2022-05-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_userbook_ratescore_usermovie_ratescore'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbook',
            name='isRated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermovie',
            name='isRated',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.0.3 on 2022-06-05 11:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_userfeed_isfollowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='report',
            name='updatedAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

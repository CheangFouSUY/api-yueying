# Generated by Django 4.0.3 on 2022-05-02 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_report_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='createdAt',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='updatedAt',
        ),
    ]

# Generated by Django 4.0.3 on 2022-05-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_usergroup_ismainadmin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='groupAdminApply',
            new_name='groupAdminRequest',
        ),
    ]
